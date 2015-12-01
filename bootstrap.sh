#!/bin/bash

# Update
apt-get update

# Install Package Dependencies
apt-get install python-pip python-dev sqlite3 -y

# Install Application from Setup
cd /var/www
pip install -r requirements.txt

# Start Flask App
cd /var/www
python manage.py runserver --host="0.0.0.0"
