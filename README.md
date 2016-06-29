# braindump

BrainDump is a simple, powerful, and open note taking platform that makes it easy to organize your life. It lives [here](http://braindump.pw) if you would like to check it out.

[![CI](https://circleci.com/gh/levlaz/braindump.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/levlaz/braindump)
![MIT License](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Docker Repository on Quay](https://quay.io/repository/levlaz/braindump/status "Docker Repository on Quay")](https://quay.io/repository/levlaz/braindump)

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

* [Dev Blog](https://levlaz.org/tag/braindump/)
* [Roadmap](https://github.com/levlaz/braindump/issues?q=is%3Aopen+is%3Aissue+label%3Afeature)

# Screenshots

## Organize your Notes with Notebooks
![Notebooks](https://github.com/levlaz/braindump/blob/master/app/static/images/notebooks.png)

## Powerful Markdown based Editing with [Prose Mirror](https://prosemirror.net/)
![New Note](https://github.com/levlaz/braindump/blob/master/app/static/images/new_note.png)

## All of your Notes in One Place
![All Notes](https://github.com/levlaz/braindump/blob/master/app/static/images/all_notes.png)

# Development

The easiest way to hack on braindump is with Vagrant

## Requirements
1. VirtualBox
2. Vagrant 
3. Git 

## Development Instructions
1. Fork and Clone this repo locally
2. `cd` into the new repo
3. Run `vagrant up`
4. Go to localhost:5000 to view the app, any changes you make locally will be reflected in the Vagrant environment.

# Deployment
The only official method of deploying Braindump is with Docker. Braindump.pw is currently running on an Ubuntu 16.04 LTS server on [Digital Ocean](https://m.do.co/c/ffc7002f7299). You can view `scripts/deploy.sh` to see how braindump is currently being deployed to production.

## Requirements
1. Docker and Docker Compose
2. SMTP (Required for Creating new Accounts and Sharing Notes)

## Deployment Instructions
1. Log into your Production Server and install Docker and Docker Compose
2. Create a new directory for braindump `mkdir -p /var/www/braindump`
3. Edit `scripts/secrets.sh` and add your site specific environment credentials.
4. Edit `etc/conf/nginx.conf` and add your site specific nginx configuration
5. From your local repo, send latest scripts to production Server

    ```
    rsync -avz scripts/ $USER@SERVER:/var/www/braindump/scripts/
    rsync -avz etc/ $USER@SERVER:/var/www/braindump/etc/
    scp docker-compose.yml $USER@SERVER:/var/www/braindump
    ```
    
6. From your local repo, log into production server, pull and restart Docker

    ```
    ssh $USER@SERVER 'cd /var/www/braindump && docker-compose pull'
    ssh $USER@SERVER 'cd /var/www/braindump && docker-compose build'
    ssh $USER@SERVER 'cd /var/www/braindump && source scripts/secrets.sh && docker-compose up -d'
    ```
    
7. (Optional) to set up automatic backups (every 6 hours) add the backup script to your crontab `crontab scripts/braindump-backup`

If all goes well, you will be able to navigate to $YOUR_SERVER in a browser and see the app. If you get a bad gateway error, or some other error try to run docker-compose in the foreground to get additional logging `cd /var/www/braindump && source scripts/secrets.sh && docker-compose up`

Test build
