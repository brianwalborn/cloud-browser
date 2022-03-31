import flask
from cloud_browser.blueprints.utils.breadcrumb import Breadcrumb
from cloud_browser.blueprints.utils.validator import Validator
from cloud_browser.models.aws.ec2.instance import Instance
from cloud_browser.tasks.send_ssm_command import SendSsmCommand
from flask import Blueprint, flash, render_template, request

class Context:
    def __init__(self):
        self.all_instances: list[Instance] = []
        self.selected_instances: list[Instance] = []
        self.sent_commands = []

    def clear(self):
        self.all_instances: list[Instance] = []
        self.selected_instances: list[Instance] = []
        self.sent_commands = []

bp = Blueprint('ssm', __name__)
context = Context()
validator = Validator()

@bp.route('/ssm/send_ssm_command/command_input', methods = ('GET', 'POST'))
def command_input():
    operating_systems = set()
    validator.invalid_fields.clear()

    try:
        if request.method == 'POST' and validator.validate_required_fields(request.form):
            if ('linux_command' in request.form or 'windows_command' in request.form):
                task = SendSsmCommand()

                if 'linux_command' in request.form: task.linux_command = request.form['linux_command']
                if 'windows_command' in request.form: task.windows_command = request.form['windows_command']

                context.sent_commands = task.send_commands(context.selected_instances)

                return flask.redirect('/ssm/send_ssm_command/command_results')
        else:
            if len(context.selected_instances):
                for instance in context.selected_instances:
                    operating_systems.add(instance.operating_system.lower())
            else:
                flash('No instances selected', 'warning')
    except Exception as e:
        flash(e, 'error')

    return render_template(
        'ssm/send_ssm_command/command_input.html',
        breadcrumbs = Breadcrumb.get_breadcrumbs(request.path),
        content_title = 'Enter Command(s)',
        instances = context.selected_instances,
        invalid_fields = validator.invalid_fields,
        operating_systems = operating_systems,
        service = 'send_ssm_command'
    )

@bp.route('/ssm/send_ssm_command/command_results')
def command_results():
    results = []

    try:
        results = SendSsmCommand().get_command_results(context.sent_commands)

        for result in results:
            for instance in context.selected_instances:
                if result.instance_id == instance.instance_id:
                    result.instance_name = instance.name

    except Exception as e:
        flash(e, 'error')

    context.clear()
        
    return render_template(
        'ssm/send_ssm_command/command_results.html',
        breadcrumbs = Breadcrumb.get_breadcrumbs(request.path),
        content_title = 'Command Results',
        results = results,
        service = 'send_ssm_command'
    )

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
            context.all_instances = SendSsmCommand().get_instances()

            if not context.all_instances: flash('No results returned. Please review settings.', 'warning')
    except Exception as e:
        flash(e, 'error')

    return render_template(
        'ssm/send_ssm_command/select_instances.html',
        breadcrumbs = Breadcrumb.get_breadcrumbs(request.path),
        content_title = 'Select Instances',
        instances = context.all_instances,
        service = 'send_ssm_command',
        show_refresh = True,
        show_filter = True
    )
