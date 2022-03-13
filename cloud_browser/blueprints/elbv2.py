from cloud_browser.tasks.target_group_health import TargetGroupHealth
from flask import Blueprint, flash, render_template

bp = Blueprint('elbv2', __name__)

@bp.route('/elbv2/get_target_group_health')
def get_target_group_health():
    results = []

    try:
        results = TargetGroupHealth().get_target_group_health()
    except Exception as e:
        flash(e, 'error')

    return render_template('elbv2/target_group_health.html', target_groups = results, service = 'get_target_group_health')
