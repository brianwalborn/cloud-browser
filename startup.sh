#!/bin/bash
export FLASK_APP=cloud_browser

if [[ $* == *--d* ]]; then
    flask init-database
fi

flask run
