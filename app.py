from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, url_for
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
SLIC3R_EXECUTABLE = 'C:\\Program Files\\Prusa3D\\PrusaSlicer\\prusa-slicer-console.exe'  # Update this with the path to your Slic3r executable

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    options = [
        {'name': 'layer_height', 'description': 'Layer Height (mm)'},
        {'name': 'infill_density', 'description': 'Infill Density (%)'},
        {'name': 'perimeters', 'description': 'Number of Perimeters'},
        {'name': 'support_material', 'description': 'Enable Support Material', 'type': 'checkbox'},
        {'name': 'support_material_spacing', 'description': 'Support Material Spacing (mm)', 'type': 'text'},
        {'name': 'support_material_style', 'description': 'Support Material Style (grid/snug/organic)', 'type': 'text'},
        {'name': 'support_tree_angle', 'description': 'Support Tree Angle (°)', 'type': 'text'},
        {'name': 'support_tree_tip_diameter', 'description': 'Support Tree Tip Diameter (mm)', 'type': 'text'},
    ]

    config_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.ini')]

    return render_template('index.html', options=options, config_files=config_files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    config_file = None
    if 'config_file' in request.files:
        config = request.files['config_file']
        if config.filename != '':
            config_filename = secure_filename(config.filename)
            config_file = os.path.join(app.config['UPLOAD_FOLDER'], config_filename)
            config.save(config_file)

    options = request.form.to_dict()
    cli_args = []

    for key, value in options.items():
        if key == 'support_material' and value == 'on':
            cli_args.append(f'--{key}')
        elif value:
            cli_args.append(f'--{key}={value}')

    output_file = os.path.join(app.config['OUTPUT_FOLDER'], f"{os.path.splitext(filename)[0]}.gcode")

    try:
        slic3r_command = [SLIC3R_EXECUTABLE, filepath, *cli_args, '--output', output_file, '--slice']
        if config_file:
            slic3r_command.extend(['--load', config_file])
        subprocess.run(slic3r_command, check=True)
    except subprocess.CalledProcessError as e:
        return f"Error during slicing: {str(e)}", 500

    return f"File sliced successfully! <a href='/download/{os.path.basename(output_file)}'>Download G-code</a>"

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

@app.route('/save_config', methods=['POST'])
def save_config():
    config_name = request.form.get('config_name')
    if 'config_file' not in request.files:
        return "No config file part", 400

    config_file = request.files['config_file']
    if config_file.filename == '':
        return "No selected config file", 400

    config_filename = secure_filename(config_name + '.ini')
    config_path = os.path.join(app.config['UPLOAD_FOLDER'], config_filename)
    config_file.save(config_path)

    return redirect(url_for('index'))

@app.route('/delete_config/<config_name>', methods=['POST'])
def delete_config(config_name):
    config_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(config_name))
    if os.path.exists(config_path):
        os.remove(config_path)
        return redirect(url_for('index'))
    else:
        return "Config file not found", 404

if __name__ == '__main__':
    app.run(debug=True)
