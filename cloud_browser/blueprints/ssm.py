import flask
import json
import os
from cloud_browser.models.aws.ec2.instance import Instance
from cloud_browser.services.custom.send_ssm_command import Orchestrator
from flask import current_app as app
from flask import Blueprint, flash, render_template, request, url_for

bp = Blueprint('ssm', __name__)

class Context:
    def __init__(self):
        self.all_instances: list[Instance] = []
        self.selected_instances: list[Instance] = []
        self.sent_commands = []

    def clear(self):
        self.all_instances: list[Instance] = []
        self.selected_instances: list[Instance] = []
        self.sent_commands = []

context = Context()

@bp.route('/ssm/send_ssm_command/command_input', methods = ('GET', 'POST'))
def command_input():
    operating_systems = set()

    try:
        if request.method == 'POST':
            if 'linux_command' in request.form or 'windows_command' in request.form:
                orchestrator = Orchestrator()

                if 'linux_command' in request.form: orchestrator.linux_command = request.form['linux_command']
                if 'windows_command' in request.form: orchestrator.windows_command = request.form['windows_command']

                context.sent_commands = orchestrator.send(context.selected_instances)

                return flask.redirect('/ssm/send_ssm_command/command_results')
        else:
            if len(context.selected_instances):
                for instance in context.selected_instances:
                    operating_systems.add(instance.operating_system.lower())
            else:
                flash('No instances selected', 'warning')
    except Exception as e:
        flash(e, 'error')

    return render_template('ssm/send_ssm_command/command_input.html', instances = context.selected_instances, operating_systems = operating_systems, service = 'send_ssm_command')

@bp.route('/ssm/send_ssm_command/command_results')
def command_results():
    results = []

    try:
        orchestrator = Orchestrator()
        results = orchestrator.get_command_results(context.sent_commands)

        for result in results:
            for instance in context.selected_instances:
                if result.instance_id == instance.instance_id:
                    result.instance_name = instance.name

    except Exception as e:
        flash(e, 'error')

    context.clear()
        
    return render_template('ssm/send_ssm_command/command_results.html', results = results, service = 'send_ssm_command')

@bp.route('/ssm')
def index():
    f = open(os.path.join(app.static_folder, 'data', 'services.json'))
    services = json.load(f)
    actions = []

    for service in services: 
        if service['name'] == 'ssm': actions = service['actions']

    return render_template('actions.html', service = 'ssm', actions = actions)

@bp.route('/ssm/send_ssm_command')
def redirect():
    return flask.redirect("/ssm/send_ssm_command/select_instances")

@bp.route('/ssm/send_ssm_command/select_instances', methods = ('GET', 'POST'))
def select_instances():
    try:
        if request.method == 'POST':
            selected = ','.join(request.form.getlist('instances'))

            for instance_id in selected.split(','):
                for instance in context.all_instances:
                    if instance.instance_id == instance_id: context.selected_instances.append(instance)

            return flask.redirect('/ssm/send_ssm_command/command_input')
        else:
            context.clear()
            orchestrator = Orchestrator()
            context.all_instances = orchestrator.fetch_instances()
    except Exception as e:
        flash(e, 'error')

    return render_template('ssm/send_ssm_command/select_instances.html', instances = context.all_instances, service = 'send_ssm_command')
