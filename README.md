# braindump

BrainDump is a simple, powerful, and open note taking platfform that makes it easy to organize your life. It lives [here](http://braindump.pw) if you would like to check it out. :)

[![CI](https://circleci.com/gh/levlaz/braindump.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/levlaz/braindump) ![MIT License](https://img.shields.io/github/license/mashape/apistatus.svg) [![Join the chat at https://gitter.im/levlaz/braindump](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/levlaz/braindump?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

# Features

Braindump is under heavy development and features are being added every week. Some highlights are:

* RESTful API (WIP)
* Full Markdown Editing
* Full Markdown Viewing
* Share Notes via Email
* Categorize Notes into Notebooks
* Categorize Notes with Tags
* Full Text Search
* Mark notes as Favorites

See something missing? Add a [feature-request](https://github.com/levlaz/braindump/issues)!

# Screenshots

![UI V2](https://cloud.githubusercontent.com/assets/7981032/11611650/4d811b74-9ba6-11e5-8159-b1d924997bc2.png)

# Deployment

I am building [docker images](https://hub.docker.com/r/levlaz/braindump/) which make it super easy to deploy braindump.

Requirements:

1. PostgreSQL Database
2. SMTP (Required for Creating new Accounts and Sharing Notes)

# Development

* [Dev Blog](https://levlaz.org/tag/braindump/)
* [Roadmap](https://github.com/levlaz/braindump/issues?q=is%3Aopen+is%3Aissue+label%3Afeature)

## Develop with Vagrant

1. Install [Vagrant](https://www.vagrantup.com/)
2. Fork and clone this repo
3. From the root of the project, run `vagrant up` in a terminal
4. Navigate to localhost:5000 to view the app in your browser

## Local development with virtualenv

1. Install virtualenv: `pip install virtualenv`
2. Fork and clone this repo
3. From the root of the project, create your virtualenv: `virtualenv env`
4. Source your virtual environment: `source env/bin/activate`
5. Install all dependencies: `pip install -r requirements.txt`
6. Start the app: `python manage.py runserver`
7. Navigate to localhost:5000 to view the app in your browser

# Technologies Used

braindump is an open source project that is built on top of the shoulders of giants. It could not be possible without the following awesome tools:

## Backend
0. Python
1. Flask
2. PostgreSQL
3. SQLAlchemy

## Frontend
1. Jinja
2. WTForms
3. Bootstrap
4. Marked.JS
5. ACE Editor

## Development
1. Vagrant
2. Flake8
3. Coverage

## Production 
1. Gunicorn
2. Docker
3. nginx 
