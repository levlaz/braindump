# braindump
BrainDump is a simple, powerful, and open note taking platfform that makes it easy to organize your life. It lives [here](http://braindump.pw) if you would like to check it out. :)

[![CI](https://circleci.com/gh/levlaz/braindump.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/levlaz/braindump) ![MIT License](https://img.shields.io/github/license/mashape/apistatus.svg)

# Screenshots 

![UI V2](https://cloud.githubusercontent.com/assets/7981032/11611650/4d811b74-9ba6-11e5-8159-b1d924997bc2.png)

# Development

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
