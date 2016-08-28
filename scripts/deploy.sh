#!/bin/bash

# Send Latest Scripts to Production Server
rsync -avz scripts/ root@app.levops.net:/var/www/braindump/scripts/
rsync -avz etc/ root@app.levops.net:/var/www/braindump/etc/
scp docker-compose.yml root@app.levops.net:/var/www/braindump

# Log into Production Server, Pull and Restart Docker
ssh root@app.levops.net 'cd /var/www/braindump && docker-compose pull'
ssh root@app.levops.net 'cd /var/www/braindump && docker-compose build'
ssh root@app.levops.net 'cd /var/www/braindump && source scripts/secrets.sh && docker-compose up -d'
