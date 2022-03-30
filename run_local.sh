#!/bin/bash
export FLASK_APP=cloud_browser

flask init-database
flask run
