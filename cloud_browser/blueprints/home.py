import json
import os
from flask import current_app as app
from flask import Blueprint, render_template, request, url_for

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    f = open(os.path.join(app.static_folder, 'data', 'services.json'))
    services = json.load(f)

    return render_template('home.html', services = services)
