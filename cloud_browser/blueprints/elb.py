from cloud_browser.tasks.load_balancer_health import LoadBalancerHealth
from flask import Blueprint, flash, render_template

bp = Blueprint('elb', __name__)

@bp.route('/elb/get_load_balancer_health')
def get_load_balancer_health():
    load_balancers = []
    
    try:
        load_balancers.extend(LoadBalancerHealth().get_load_balancer_health())

        if not load_balancers: flash('No results returned. Please review settings.', 'warning')
    except Exception as e:
        flash(e, 'error')

    return render_template('elb/load_balancer_health.html', load_balancers = load_balancers, service = 'get_load_balancer_health')
