from cloud_browser.blueprints.utils.breadcrumb import Breadcrumb
from cloud_browser.tasks.get_auto_scaling_groups import GetAutoScalingGroups
from flask import Blueprint, flash, render_template, request

bp = Blueprint('autoscaling', __name__)

@bp.route('/autoscaling/get_life_cycle_hooks')
def get_life_cycle_hooks():
    auto_scaling_groups = []

    try:
        auto_scaling_groups.extend(GetAutoScalingGroups().get_auto_scaling_groups())
        
        if not auto_scaling_groups: flash('No results returned. Please review settings.', 'warning')
    except Exception as e:
        flash(e, 'error')

    return render_template('autoscaling/life_cycle_hooks.html', auto_scaling_groups = auto_scaling_groups, breadcrumbs = Breadcrumb.get_breadcrumbs(request.path), service = 'get_life_cycle_hooks')

@bp.route('/autoscaling/get_suspended_processes')
def get_suspended_processes():
    auto_scaling_groups = []

    try:
        auto_scaling_groups.extend(GetAutoScalingGroups().get_auto_scaling_groups())
        
        if not auto_scaling_groups: flash('No results returned. Please review settings.', 'warning')
    except Exception as e:
        flash(e, 'error')

    return render_template('autoscaling/suspended_processes.html', auto_scaling_groups = auto_scaling_groups, breadcrumbs = Breadcrumb.get_breadcrumbs(request.path), service = 'get_suspended_processes')
