from flask import current_app as app
from flask import Blueprint, render_template, request, url_for

bp = Blueprint('settings', __name__)

@bp.route('/settings')
def index():
    return render_template('settings.html', service = 'settings')
