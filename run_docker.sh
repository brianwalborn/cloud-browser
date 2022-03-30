#!/bin/bash
app="cloud-browser"
aws_credentials_path="$HOME/.aws"
docker build -t ${app} .
docker run --rm -d -p 8080:5000 -v $aws_credentials_path:/root/.aws --user=root "cloud-browser"
