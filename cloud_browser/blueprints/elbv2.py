import cloud_browser.services.custom.check_target_group_health as health
import json
import os
from flask import current_app as app
from flask import Blueprint, flash, render_template

bp = Blueprint('elbv2', __name__)

@bp.route('/elbv2')
def index():
    f = open(os.path.join(app.static_folder, 'data', 'services.json'))
    services = json.load(f)
    actions = []

    for service in services: 
        if service['name'] == 'elbv2': actions = service['actions']

    return render_template('actions.html', service = 'elbv2', actions = actions)

@bp.route('/elbv2/check_target_group_health')
def check_target_group_health():
    results = []

    try:
        results = health.check_target_group_health()
    except Exception as e:
        flash(e, 'error')

    return render_template('elbv2/check_target_group_health.html', target_groups = results, service = 'check_target_group_health')
