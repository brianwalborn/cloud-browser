from cloud_browser.blueprints.utils.breadcrumb import Breadcrumb
from cloud_browser.tasks.load_balancer_health import LoadBalancerHealth
from flask import Blueprint, flash, render_template, request

bp = Blueprint('elb', __name__)

@bp.route('/elb/get_load_balancer_health')
def get_load_balancer_health():
    load_balancers = []
    
    try:
        load_balancers.extend(LoadBalancerHealth().get_load_balancer_health())

        if not load_balancers: flash('No results returned. Please review settings.', 'warning')
    except Exception as e:
        flash(e, 'error')

    return render_template(
        'elb/load_balancer_health.html',
        breadcrumbs = Breadcrumb.get_breadcrumbs(request.path),
        content_title = 'Classic Load Balancers',
        load_balancers = load_balancers,
        service = 'get_load_balancer_health',
        show_refresh = True
    )
