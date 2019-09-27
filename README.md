![Imara Logo](screenshots/logo.png)
# Imara.api

The aim of this project is to create API endpoints that will be consumed by all the Imara apps (Android and Web app).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Install [Python](https://www.python.org/downloads/)
* Install a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

### Installing
* Clone the repo to your local machine
```
git clone https://github.com/ImaraTv/Imara.api.git
```
* cd into the project
```
cd imara.api
```
* Activate the virtual environment. Check this [link](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) on how to activate a virtual environment depending on your OS
* Install dependencies
```
pip install -r requirements.txt
```
* Run migrations
```
python manage.py makemigrations
```
```
python manage.py migrate
```
* Run the server
```
python manage.py runserver
```

## Built With
* [Django](https://www.djangoproject.com)
* [Django REST framework](https://www.django-rest-framework.org)

## Authors
* **Charles Maina**
* **Suleiman Yunus**
* **Bill Odida**