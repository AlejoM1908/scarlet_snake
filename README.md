# Scarlet Snake

This repository is designed for a backend skills and knowledge test, the main idea is to build a backend application using the framework Django and a relational database to simulate the functionalities of a homework software where the teachers can add activities for the students and the students can submit their work
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file in the classroom main directory.

### Database

`DATABASE_NAME`

`DATABASE_USER`

`DATABASE_PASSWORD`

`DATABASE_HOST`

`DATABASE_PORT`

### Django

`DJANGO_ALLOWED_HOSTS`

`SECRET_KEY`

### GCloud Bucket

`GCLOUD_CREDENTIALS`

GCLOUD_CREDENTIALS are the one-line format of the gcloud .json credentials generated by the Cloud Storage API

## Installation

Install the project with django in a virtual environment

Use the file requirement.txt to install all required libraries for the project in the scarlet_snake directory with pip:

### Linux install:
```bash
pip3 install -r requirements.txt
````

Run the django server with:
```bash
python3 manage.py makemigrations && python3 manage.py migrate
python3 manage.py runserver
```