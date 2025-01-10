from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
SLIC3R_EXECUTABLE = 'C:\\Program Files\\Prusa3D\\PrusaSlicer\\prusa-slicer-console.exe'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    options = [
#commented because a dropdown was added instead in html        {'name': 'layer-height', 'description': 'Layer Height (mm)'},
#        {'name': 'infill-density', 'description': 'Infill Density (%)'},
#        {'name': 'perimeters', 'description': 'Number of Perimeters'},
        {'name': 'support-material', 'description': 'Enable Support Material', 'type': 'checkbox'},
    ]

    config_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.ini')]

    return render_template('index.html', options=options, config_files=config_files)

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
        if key == 'support-material-style' and value == 'on':
            cli_args.append(f'organic')
        elif value:
            cli_args.append(f'--{key}={value}')

    output_file = os.path.join(app.config['OUTPUT_FOLDER'], f"{os.path.splitext(stl_filename)[0]}.gcode")

    try:
        slic3r_command = [SLIC3R_EXECUTABLE, stl_filepath, '--output', output_file, '--slice']
        if config_filepath:
            slic3r_command.extend(['--load', config_filepath])
        slic3r_command.extend(cli_args)
        subprocess.run(slic3r_command, check=True)
    except subprocess.CalledProcessError as e:
        return f"Error during slicing: {str(e)}", 500

    return f"File sliced successfully! <a href='/download/{os.path.basename(output_file)}'>Download G-code</a>"

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

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

@app.route('/delete_config/<config_name>', methods=['POST'])
def delete_config(config_name):
    config_filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(config_name))
    if os.path.exists(config_filepath):
        os.remove(config_filepath)
        return redirect(url_for('index'))
    else:
        return "Config file not found.", 404

if __name__ == '__main__':
    app.run(debug=True)
