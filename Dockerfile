# FROM tiangolo/uwsgi-nginx-flask:python3.9
# WORKDIR /app
# # Install Poetry
# RUN apt-get update \
#     && apt-get install -y ca-certificates \
#     && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python \
#     && cd /usr/local/bin \
#     && ln -s /opt/poetry/bin/poetry \
#     && poetry config virtualenvs.create false
# COPY ./ /app
# RUN poetry install --no-root
# # STATIC_PATH configures nginx to serve static assets directly
# ENV \
#     POETRY_HOME=/opt/poetry \
#     STATIC_PATH=/app/app/static \
#     FLASK_ENV=production
# EXPOSE 80

#Create a ubuntu base image with python 3 installed.
FROM python:3.10

#Set the working directory
WORKDIR /

#copy all the files
COPY . .

#Install the dependencies
RUN apt-get -y update
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install -r requirements.txt

#Expose the required port
EXPOSE 5000

#Run the command
CMD gunicorn dashapp:server