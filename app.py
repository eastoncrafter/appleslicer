from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import os
import subprocess
import requests
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
SLIC3R_EXECUTABLE = '/app/prusaslicer/prusa-slicer'
#OCTOPRINT_API_KEY = 'eP1a5wTv8q5hn3ArUFxq1Kffg8Kh0pYd-3erT1_JqlI'
#OCTOPRINT_URL = 'http://10.1.10.56/api/files/local'
#CONTINUOUSPRINTURL = 'http://10.1.10.56/plugin/continuousprint'

# reads from env variables for docker support, defaults back if none provided (supposedly...)
OCTOPRINT_API_KEY = os.environ.get('OCTOPRINT_API_KEY', 'eP1a5wTv8q5hn3ArUFxq1Kffg8Kh0pYd-3erT1_JqlI')
OCTOPRINT_URL = os.environ.get('OCTOPRINT_URL', 'http://10.1.10.56/api/files/local')
CONTINUOUSPRINTURL = os.environ.get('CONTINUOUSPRINTURL', 'http://10.1.10.56/plugin/continuousprint')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)



# Index page, renders options and list of config files
@app.route('/')
def index():
    options = [
        {'name': 'support-material', 'description': 'Enable Support Material', 'type': 'checkbox'},
    ]

    config_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.ini')]

    return render_template('index.html', options=options, config_files=config_files)


# Main Slicing function, takes the uploaded file and config file, and slices the STL file, then redirects to the sliced file page with options to download, send to octoprint, queue to octoprint, or return to home.
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or not request.files['file'].filename:
        return "No STL file provided.", 400

    stl_file = request.files['file']
    stl_filename = secure_filename(stl_file.filename)
    stl_filepath = os.path.join(app.config['UPLOAD_FOLDER'], stl_filename)
    stl_file.save(stl_filepath)

    config_file = request.form.get('selected_config')
    config_filepath = None
    if config_file:
        config_filepath = os.path.join(app.config['UPLOAD_FOLDER'], config_file)

    options = request.form.to_dict()
    cli_args = []

    for key, value in options.items():
        if key in ['selected_config', 'file']:
            continue
        if key == 'support-material' and value == 'on':
            cli_args.append(f'--{key}')
            continue
        elif value:
            cli_args.append(f'--{key}={value}')

    output_file = os.path.join(app.config['OUTPUT_FOLDER'], f"{os.path.splitext(stl_filename)[0]}.gcode")

    try:
        slic3r_command = [SLIC3R_EXECUTABLE, stl_filepath, '--output', output_file, '--slice']
        if config_filepath:
            slic3r_command.extend(['--load', config_filepath])
        slic3r_command.extend(cli_args)
        print(' '.join(slic3r_command))
        subprocess.run(slic3r_command, check=True)
    except subprocess.CalledProcessError as e:
        return f"Error during slicing: {str(e)}", 500

    return redirect(url_for('sliced_file_page', filename=os.path.basename(output_file)))





#Slice config management upload and remove functions
####################################################################################################
@app.route('/save_config', methods=['POST'])
def save_config():
    if 'config_file' not in request.files or not request.files['config_file'].filename:
        return "No config file provided.", 400

    config_file = request.files['config_file']
    config_name = request.form.get('config_name', config_file.filename)
    config_filename = secure_filename(config_name)
    config_filepath = os.path.join(app.config['UPLOAD_FOLDER'], config_filename)
    config_file.save(config_filepath)

    return redirect(url_for('index'))
#--------------------------------------------------------------------------------------------------#
@app.route('/delete_config/<config_name>', methods=['POST'])
def delete_config(config_name):
    config_filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(config_name))
    if os.path.exists(config_filepath):
        os.remove(config_filepath)
        return redirect(url_for('index'))
    else:
        return "Config file not found.", 404
####################################################################################################


###END API SECTION




#START RENDER SECTION
# Simple interface to download the gcode, push or queue to octoprint, or return to home. Accepts the filename of the gcode file so it can be passed to /download and /send_to_octoprint
@app.route('/sliced_file/<filename>')
def sliced_file_page(filename):
    return render_template('sliced_file.html', filename=filename)
# Download function for the above function
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)













#Don't know how this got here
#renders for send and queue to octoprint
#@app.route('/queue_to_octoprint/<filename>')
#def queue_to_octoprint_page(filename):
#    return render_template('queue_to_octoprint.html', filename=filename)


# Send to Octoprint
@app.route('/send_to_octoprint/<filename>', methods=['POST'])
def send_to_octoprint(filename):
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if not os.path.exists(file_path):
        return "File not found.", 404

    with open(file_path, 'rb') as file:
        response = requests.post(
            OCTOPRINT_URL,
            headers={'X-Api-Key': OCTOPRINT_API_KEY},
            files={'file': file}
        )

    if response.status_code == 201:
        return "File successfully sent to OctoPrint."
    else:
        return f"Failed to send file to OctoPrint: {response.status_code} - {response.text}", 500
# Queue to octoprint
@app.route('/queue_to_octoprint/<filename>', methods=['POST'])
def queue_to_octoprint(filename):
    printer_name = request.form.get('printer_name')
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if not os.path.exists(file_path):
        return "File not found.", 404

    with open(file_path, 'rb') as file:
        response = requests.post(
            OCTOPRINT_URL,
            headers={'X-Api-Key': OCTOPRINT_API_KEY},
            files={'file': file}
        )

    if response.status_code == 201:
        headers = {
        "Authorization": "Bearer eP1a5wTv8q5hn3ArUFxq1Kffg8Kh0pYd-3erT1_JqlI",  # Replace <your-token> with the actual token
        "Content-Type": "application/json"
      }
        queue_response = requests.post(
            url=CONTINUOUSPRINTURL + '/set/add',
            headers={
                "Authorization": "Bearer iggUK5dwXCiO66NQIZKl06oIjWL1c9_mpWTIu2GZ4ps", # Replace <your-token> with the actual token
            },
            files={
                'json': (None, json.dumps({
                    "path": filename,  # dynamically post with the filename provided
                    "sd": False,
                    "count": 1,
                    "jobDraft": False,
                    "queue": "local",
                    "profiles": ["Creality Ender 3"]
                }))
            }
        )
        print(queue_response)
        if queue_response.status_code == 200:

            return "File successfully queued to OctoPrint."
        else:
                return f"Failed to queue file: {queue_response.status_code} - {queue_response.text}", 500







if __name__ == '__main__':
    app.run(debug=True)
