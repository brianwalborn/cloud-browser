import os
from cloud_browser.blueprints import autoscaling, base, ec2, elb, elbv2, settings, ssm
from cloud_browser.database import database
from flask import Flask

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config = True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'cloud_browser.sqlite'),
    )

    if test_config is None: app.config.from_pyfile('config.py', silent = True)
    else: app.config.from_mapping(test_config)

    try: os.makedirs(app.instance_path)
    except OSError: pass

    app.register_blueprint(autoscaling.bp)
    app.add_url_rule('/autoscaling/<string:task>', endpoint = '')

    app.register_blueprint(ec2.bp)
    app.add_url_rule('/ec2/<string:task>', endpoint = '')

    app.register_blueprint(elb.bp)
    app.add_url_rule('/elb/<string:task>', endpoint = '')

    app.register_blueprint(elbv2.bp)
    app.add_url_rule('/elbv2/<string:task>', endpoint = '')

    app.register_blueprint(base.bp)
    app.add_url_rule('/', endpoint = 'index')

    app.register_blueprint(settings.bp)
    app.add_url_rule('/settings', endpoint = 'index')

    app.register_blueprint(ssm.bp)
    app.add_url_rule('/ssm/<string:task>', endpoint = '')

    database.init_app(app)

    return app

