#!/bin/bash

# Send Latest Scripts to Production Server
rsync -avz scripts/ circle@hydrogen.levlaz.org:/var/www/braindump/scripts/
rsync -avz etc/ circle@hydrogen.levlaz.org:/var/www/braindump/etc/
scp docker-compose.yml circle@hydrogen.levlaz.org:/var/www/braindump

# Log into Production Server, Pull and Restart Docker
ssh circle@hydrogen.levlaz.org 'cd /var/www/braindump && docker-compose pull'
ssh circle@hydrogen.levlaz.org 'cd /var/www/braindump && docker-compose build'
ssh circle@hydrogen.levlaz.org 'cd /var/www/braindump && source scripts/secrets.sh && docker-compose up -d'
