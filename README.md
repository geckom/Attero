# Attero

## Unstable pre-alpha software - Not not use on production systems

.. image:: https://secure.travis-ci.org/geckom/Attero.png?branch=master
    :alt: Build Status
    :target: https://travis-ci.org/geckom/Attero

### A report writing and collaboration tool for infosec
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

