#!/bin/bash

# Send Latest Scripts to Production Server
rsync -avz scripts/ circleci@159.203.236.126:/var/www/braindump/scripts/
rsync -avz etc/ circleci@159.203.236.126:/var/www/braindump/etc/
scp docker-compose.yml circleci@159.203.236.126:/var/www/braindump

# Log into Production Server, Pull and Restart Docker
ssh circleci@159.203.236.126 'cd /var/www/braindump && docker-compose pull'
ssh circleci@159.203.236.126 'cd /var/www/braindump && docker-compose build'
ssh circleci@159.203.236.126 'cd /var/www/braindump && source scripts/secrets.sh && docker-compose up -d'