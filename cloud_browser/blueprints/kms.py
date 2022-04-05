from cloud_browser.blueprints.utils.breadcrumb import Breadcrumb
from cloud_browser.blueprints.utils.validator import Validator
from cloud_browser.database.database import get_database
from cloud_browser.services.aws.kms import KeyManagementServiceService
from flask import Blueprint, flash, render_template, request

bp = Blueprint('kms', __name__)
validator = Validator()
validator.immune_fields = ['context_key', 'context_value']

@bp.route('/kms/decrypt_ciphertext', methods = ('GET', 'POST'))
def decrypt_ciphertext():
    regions = get_database().execute('SELECT * FROM settings_query_regions').fetchall()
    result = None

    try:
        validator.invalid_fields.clear()

        if request.method == 'POST':
            if 'context_key' in request.form and request.form['context_key']: validator.immune_fields.remove('context_value')
            if 'context_value' in request.form and request.form['context_value']: validator.immune_fields.remove('context_key')

            if validator.validate_required_fields(request.form):
                encryption_context = None

                if 'context_key' in request.form and request.form['context_key']: encryption_context = {f'{request.form["context_key"]}': f'{request.form["context_value"]}'}

                result = KeyManagementServiceService(request.form['region']).decrypt(request.form['ciphertext'], encryption_context)
    except Exception as e:
        result = None
        flash(e, 'error')

    reset_immune_fields()

    return render_template(
        'kms/decrypt_ciphertext.html',
        breadcrumbs = Breadcrumb.get_breadcrumbs(request.path),
        content_title = 'Decrypt Ciphertext',
        invalid_fields = validator.invalid_fields,
        regions = regions,
        result = result,
        service = 'decrypt_ciphertext'
    )

@bp.route('/kms/encrypt_plaintext', methods = ('GET', 'POST'))
def encrypt_plaintext():
    regions = get_database().execute('SELECT * FROM settings_query_regions').fetchall()
    result = None

    try:
        validator.invalid_fields.clear()

        if request.method == 'POST':
            if 'context_key' in request.form and request.form['context_key']: validator.immune_fields.remove('context_value')
            if 'context_value' in request.form and request.form['context_value']: validator.immune_fields.remove('context_key')

            if validator.validate_required_fields(request.form):
                encryption_context = None

                if 'context_key' in request.form and request.form['context_key']: encryption_context = {f'{request.form["context_key"]}': f'{request.form["context_value"]}'}

                result = KeyManagementServiceService(request.form['region']).encrypt(request.form['key'], request.form['plaintext'], encryption_context)
    except Exception as e:
        result = None
        flash(e, 'error')

    reset_immune_fields()

    return render_template(
        'kms/encrypt_plaintext.html',
        breadcrumbs = Breadcrumb.get_breadcrumbs(request.path),
        content_title = 'Encrypt Plaintext',
        invalid_fields = validator.invalid_fields,
        regions = regions,
        result = result,
        service = 'encrypt_plaintext'
    )

def reset_immune_fields() -> None:
    validator.immune_fields = ['context_key', 'context_value']
