# Attero

## Unstable pre-alpha software - Do not use on production systems

[![Build Status](https://travis-ci.org/geckom/Attero.svg?branch=master)](https://travis-ci.org/geckom/Attero)
[![Requirements Status](https://requires.io/github/geckom/Attero/requirements.svg?branch=master)](https://requires.io/github/geckom/Attero/requirements/?branch=master)
[![codecov](https://codecov.io/gh/geckom/Attero/branch/master/graph/badge.svg)](https://codecov.io/gh/geckom/Attero)

### A note taking tool for infosec
Attero is a note taking, report generating, collaboration and management tool designed primary for pentetration testing and red team engagements.

## Installation

The installation:
* Install python3 and django 

* Install the python requirements 

### Ubuntu installation

* Install the following packages "apt install python3 python3-django python3-pip"

* Install the pip packages "pip3 -r requirements.txt"

## Post-Installation : Getting Started

Initialize the database:
```
python3 manage.py migrate
```

And then create the administration user:
```
python3 manage.py createsuperuser
```

Start Attero:
```
python3 manage.py runserver
```

## Features

* Simple project management system

* Tree structured notes per project

* Notes created in HTML using a WYSIWYG editor

* Task management system per project

## Work in progress

[x] Create basic project system
[x] Setup basic template
[x] Setup User management system
[x] Setup project object based permissions
[x] Create note system (tree structured)
[x] Create task system (tree structured)
[ ] Update menu styling (for in-project pages)
[ ] Create nmap import feature
