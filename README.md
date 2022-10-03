# Bakery Inventory Management System


## Table of Contents

- [About](#about)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Author](#author)

## About <a name = "about"></a>

An Inventory and Process Management tool for a bakery.

## Project Structure <a name = "project-structure"></a>


```bash

├── apps
│   ├── bakeryadmin
│   │   ├── migrations
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── commons
│   │   ├── migrations
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── inventory
│   │   ├── migrations
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── dependencies
│   │   │   └── constants.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── users
│   │   ├── migrations
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── dependencies
│   │   │   └── constants.py
│   │   ├── forms.py
│   │   ├── managers.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tasks.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── utility
├── core
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── .env
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── setup.cfg
└── README.md
```

## Prerequisites <a name = "prerequisites"></a>

- Python 3.10
- PostgreSQL 14
- Redis

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

 - Run `git clone https://github.com/seun-beta/Bakery-API` to clone the project locally.
 - Create a local postgres database locally and add it's url to the DATBASE_URL env variable.
 - Run `pip install -r requirements/development.txt`
 - Run migration with `python manage.py migrate`.


Now, make sure to have 3 extra terminals/command prompts for the following commands:
1) To run the redis server: `redis-server`
2) Start the app with `python manage.py runserver`
3) To run celery: `python -m celery -A core worker`
4) To run flower: `celery -A core flower`


## Author <a name = "author"></a>
This software was created by Seunfunmi Adegoke, a Backend & Cloud Engineer