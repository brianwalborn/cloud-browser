import boto3
from cloud_browser.blueprints.utils.breadcrumb import Breadcrumb
from cloud_browser.blueprints.utils.validator import Validator
from cloud_browser.database.database import get_database
from flask import Blueprint, flash, render_template, request

bp = Blueprint('settings', __name__)
validator = Validator()
validator.immune_fields = ['add_excluded_tag', 'add_region', 'add_session', 'add_tag', 'remove_excluded_tag', 'remove_region', 'remove_session', 'remove_tag', 'select_aws_profile'] # field names that do not get validated

@bp.route('/settings', methods = ('GET', 'POST'))
def index():
    database = get_database()
    validator.invalid_fields.clear()

    if request.method == 'POST':
        try:
            if validator.validate_required_fields(request.form):
                if 'select_aws_profile' in request.form:
                    database.execute('UPDATE settings_selected_aws_profile SET aws_profile = (?)', (request.form['aws_profile'],))
                elif 'add_region' in request.form:
                    database.execute('INSERT INTO settings_query_regions (region) VALUES (?)', (request.form['region'],))
                elif 'remove_region' in request.form:
                    database.execute('DELETE FROM settings_query_regions WHERE id = (?)', (request.form['id'],))
                elif 'add_tag' in request.form:
                    database.execute('INSERT INTO settings_query_tags (tag_key, tag_value) VALUES (?, ?)', (request.form['key'], request.form['value'],))
                elif 'remove_tag' in request.form:
                    database.execute('DELETE FROM settings_query_tags WHERE id = (?)', (request.form['id'],))
                elif 'add_excluded_tag' in request.form:
                    database.execute('INSERT INTO settings_exclude_tags (tag_key, tag_value) VALUES (?, ?)', (request.form['excluded_key'], request.form['excluded_value'],))
                elif 'remove_excluded_tag' in request.form:
                    database.execute('DELETE FROM settings_exclude_tags WHERE id = (?)', (request.form['id'],))
                elif 'add_session' in request.form:
                    database.execute('INSERT INTO settings_putty_session_names (region, session_name) VALUES (?, ?)', (request.form['session_region'], request.form['session_name'],))
                elif 'remove_session' in request.form:
                    database.execute('DELETE FROM settings_putty_session_names WHERE id = (?)', (request.form['id'],))

                database.commit()
        except Exception as e:
            flash(e, 'error')

    aws_profiles = sorted(boto3.Session().available_profiles)
    putty_sessions = database.execute('SELECT * FROM settings_putty_session_names').fetchall()
    regions = database.execute('SELECT * FROM settings_query_regions').fetchall()
    selected_aws_profile = database.execute('SELECT * FROM settings_selected_aws_profile').fetchone()
    tags = database.execute('SELECT * FROM settings_query_tags').fetchall()
    tags_to_exclude = database.execute('SELECT * FROM settings_exclude_tags').fetchall()

    return render_template(
        'settings.html',
        aws_profiles = aws_profiles,
        breadcrumbs = Breadcrumb.get_breadcrumbs(request.path),
        content_title = 'Settings',
        invalid_fields = validator.invalid_fields,
        putty_sessions = putty_sessions,
        regions = regions,
        selected_aws_profile = selected_aws_profile['aws_profile'],
        service = 'settings',
        tags = tags,
        tags_to_exclude = tags_to_exclude
    )
