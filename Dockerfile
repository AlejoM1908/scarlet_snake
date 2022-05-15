FROM python:3.10.1-alpine

WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip 
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt

COPY . /usr/src/app
RUN python manage.py makemigrations && python manage.py migrate
CMD python manage.py runserver 0.0.0.0:$PORT