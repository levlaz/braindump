#!/bin/bash

# Send Latest Scripts to Production Server
rsync -avz scripts/ circleci@app.levops.net:/var/www/braindump/scripts/
rsync -avz etc/ circleci@app.levops.net:/var/www/braindump/etc/
scp docker-compose.yml circleci@app.levops.net:/var/www/braindump

# Log into Production Server, Pull and Restart Docker
ssh circleci@app.levops.net 'cd /var/www/braindump && docker-compose pull'
ssh circleci@app.levops.net 'cd /var/www/braindump && docker-compose build'
ssh circleci@app.levops.net 'cd /var/www/braindump && source scripts/secrets.sh && docker-compose up -d'
