import json
import os
from cloud_browser.blueprints.utils.breadcrumb import Breadcrumb
from flask import current_app as app
from flask import Blueprint, render_template, request

bp = Blueprint('base', __name__)

@bp.route('/')
def index():
    f = open(os.path.join(app.static_folder, 'data', 'services.json'))
    services = json.load(f)

    return render_template(
        'shared/services.html',
        content_title = 'AWS Services',
        services = services
    )

@bp.route('/<string:service>')
def load_tasks(service):
    f = open(os.path.join(app.static_folder, 'data', 'services.json'))
    services = json.load(f)
    tasks = []

    for aws_service in services: 
        if aws_service['name'] == service: tasks = aws_service['tasks']

    return render_template(
        'shared/tasks.html',
        breadcrumbs = Breadcrumb.get_breadcrumbs(request.path),
        service = service, tasks = tasks
    )
