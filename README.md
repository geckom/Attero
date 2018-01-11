# Attero

## Unstable pre-alpha software - Not not use on production systems

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
python3 manage.py createsuperuse
```

Start Attero:
```
python3 manage.py runserver
```

## About Attero
Serpico is at its core a report generation tool but targeted at creating information security reports. When building a report the user adds "findings" from the template database to the report. When there are enough findings, click 'Generate Report' to create the docx with your findings. The docx design comes from a Report Template which can be added through the UI; a default one is included. The Report Templates use a custom Markup Language to stub the data from the UI (i.e. findings, customer name, etc) and put them into the report.

## Features

* Simple project management system

* Tree structured notes per project

* Notes created in HTML using a WYSIWYG editor

* Task management system per project

