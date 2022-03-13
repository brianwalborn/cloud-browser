from cloud_browser.blueprints.utils.breadcrumb import Breadcrumb
from cloud_browser.tasks.generate_conf_cons import GenerateConfCons
from flask import Blueprint, flash, render_template, request

bp = Blueprint('ec2', __name__)

@bp.route('/ec2/generate_conf_cons')
def generate_conf_cons():
    xml = ''
    
    try:
        xml = GenerateConfCons().generate()
    except Exception as e:
        flash(e, 'error')

    return render_template('ec2/generate_conf_cons.html', breadcrumbs = Breadcrumb.get_breadcrumbs(request.path), service = 'generate_conf_cons', xml = xml)
