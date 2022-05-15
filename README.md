# Scarlet Snake

This repository is designed for a backend skills and knowledge test, the main idea is to build a backend application using the framework Django and a relational database to simulate the functionalities of a homework software where the teachers can add activities for the students and the students can submit their work
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file in the classroom main directory.

`DATABASE_NAME`

`DATABASE_USER`

`DATABASE_PASSWORD`

`DATABASE_HOST`

`DATABASE_PORT`

## Installation

Install the project with django in a virtual environment

Use the file requirement.txt to install all required libraries for the project in the scarlet_snake directory with pip:

### Linux install:
```bash
pip3 install -r requirements.txt
````

Run the django server with:
```bash
cd classroom
python3 manage.py runserver
```

### Windows install:
```bash
pip install -r requirements.txt
```

Run the django server with:
```bash
    CD classroom
    py manage.py runserver
```