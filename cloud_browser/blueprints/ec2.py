import json
import os
from cloud_browser.services.custom.generate_conf_cons import Generator
from flask import current_app as app
from flask import Blueprint, flash, render_template

bp = Blueprint('ec2', __name__)

@bp.route('/ec2')
def index():
    f = open(os.path.join(app.static_folder, 'data', 'services.json'))
    services = json.load(f)
    actions = []

    for service in services: 
        if service['name'] == 'ec2': actions = service['actions']

    return render_template('actions.html', service = 'ec2', actions = actions)

@bp.route('/ec2/generate_conf_cons')
def generate_conf_cons():
    xml = ''
    
    try:
        generator = Generator()
        xml = generator.run()
    except Exception as e:
        flash(e, 'error')

    return render_template('ec2/generate_conf_cons.html', service = 'generate_conf_cons', xml = xml)
