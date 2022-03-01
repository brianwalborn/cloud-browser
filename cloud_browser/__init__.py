import os
from cloud_browser.blueprints import autoscaling, elb, home, settings
from flask import Flask

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config = True)

    if test_config is None: app.config.from_pyfile('config.py', silent = True)
    else: app.config.from_mapping(test_config)

    try: os.makedirs(app.instance_path)
    except OSError: pass

    app.register_blueprint(autoscaling.bp)
    app.add_url_rule('/autoscaling', endpoint = 'index')

    app.register_blueprint(elb.bp)
    app.add_url_rule('/elb', endpoint = 'index')

    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint = 'index')

    app.register_blueprint(settings.bp)
    app.add_url_rule('/settings', endpoint = 'index')

    return app
