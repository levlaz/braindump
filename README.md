# braindump

BrainDump is a simple, powerful, and open note taking platform that makes it easy to organize your life. It lives [here](http://braindump.pw) if you would like to check it out. :)

[![CI](https://circleci.com/gh/levlaz/braindump.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/levlaz/braindump)

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

## Note Editor 
![UI V2](https://github.com/levlaz/braindump/blob/master/app/static/images/outer_edit.png)

## Note View 
![UI V2](https://github.com/levlaz/braindump/blob/master/app/static/images/outer_preview.png)

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
