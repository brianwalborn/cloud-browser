import json
import os
from cloud_browser.services.custom.check_load_balancer_health import Check
from flask import current_app as app
from flask import Blueprint, render_template, request, url_for

bp = Blueprint('elb', __name__)

@bp.route('/elb')
def index():
    f = open(os.path.join(app.static_folder, 'data', 'services.json'))
    services = json.load(f)
    actions = []

    for service in services: 
        if service['name'] == 'elb': actions = service['actions']

    return render_template('actions.html', service = 'elb', actions = actions)

@bp.route('/elb/check_load_balancer_health')
def check_load_balancer_health():
    check = Check()
    load_balancers = check.get_load_balancer_instance_health()

    return render_template('elb/check_load_balancer_health.html', load_balancers = load_balancers, service = 'check_load_balancer_health')
