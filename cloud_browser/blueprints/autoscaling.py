import json
import os
from cloud_browser.services.custom.check_auto_scaling_groups import Scanner
from flask import current_app as app
from flask import Blueprint, render_template, request, url_for

bp = Blueprint('autoscaling', __name__)

@bp.route('/autoscaling')
def index():
    f = open(os.path.join(app.static_folder, 'data', 'services.json'))
    services = json.load(f)
    actions = []

    for service in services: 
        if service['name'] == 'autoscaling': actions = service['actions']

    return render_template('actions.html', service = 'autoscaling', actions = actions)

@bp.route('/autoscaling/check_auto_scaling_groups')
def check_auto_scaling_groups():
    scanner = Scanner()
    auto_scaling_groups = scanner.get_auto_scaling_groups()

    return render_template('autoscaling/check_auto_scaling_groups.html', auto_scaling_groups = auto_scaling_groups, service = 'check_auto_scaling_groups')