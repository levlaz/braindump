#!/bin/bash

# Send Latest Scripts to Production Server
rsync -avz scripts/ $PROD_SERVER:/var/www/braindump/scripts/
rsync -avz etc/ $PROD_SERVER:/var/www/braindump/etc/
scp docker-compose.yml $PROD_SERVER:/var/www/braindump

# Log into Production Server, Pull and Restart Docker
ssh $PROD_SERVER 'cd /var/www/braindump && docker-compose pull'
ssh $PROD_SERVER 'cd /var/www/braindump && docker-compose build'
ssh $PROD_SERVER 'cd /var/www/braindump && source scripts/secrets.sh && docker-compose up -d'
