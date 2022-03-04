from cloud_browser.database.database import get_database
from flask import current_app as app
from flask import Blueprint, flash, render_template, request, url_for

bp = Blueprint('settings', __name__)

@bp.route('/settings', methods = ('GET', 'POST'))
def index():
    database = get_database()

    if request.method == 'POST':
        try:
            if 'add_region' in request.form:
                database.execute('INSERT INTO settings_query_regions (region) VALUES (?)', (request.form['region'],))
            elif 'remove_region' in request.form:
                database.execute('DELETE FROM settings_query_regions WHERE id = (?)', (request.form['id'],))
            elif 'add_tag' in request.form:
                database.execute('INSERT INTO settings_query_tags (tag_key, tag_value) VALUES (?, ?)', (request.form['key'], request.form['value'],))
            elif 'remove_tag' in request.form:
                database.execute('DELETE FROM settings_query_tags WHERE id = (?)', (request.form['id'],))
            elif 'add_excluded_tag' in request.form:
                database.execute('INSERT INTO settings_exclude_tags (tag_key, tag_value) VALUES (?, ?)', (request.form['key'], request.form['value'],))
            elif 'remove_excluded_tag' in request.form:
                database.execute('DELETE FROM settings_exclude_tags WHERE id = (?)', (request.form['id'],))

            database.commit()
        except Exception as e:
            flash(e)
            print(e)

    regions = database.execute('SELECT * FROM settings_query_regions').fetchall()
    tags = database.execute('SELECT * FROM settings_query_tags').fetchall()
    tags_to_exclude = database.execute('SELECT * FROM settings_exclude_tags').fetchall()

    return render_template('settings.html', regions = regions, service = 'settings', tags = tags, tags_to_exclude = tags_to_exclude)
