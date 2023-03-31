# Pulling the base image

FROM python:3.11-slim-bullseye

# Setting root directory of the application

WORKDIR /app

# Copying requirements file from the local filesystem

COPY ./requirements.txt /app/requirements.txt

# Creating and activating a virtual environment and installing the dependencies

RUN python3 -m venv venv && \
    /bin/bash -c ". venv/bin/activate && \
    pip install --no-cache-dir --upgrade -r /app/requirements.txt"

# Copying main script from the local filesystem

COPY ./main.py /app/main.py

# Copying the contents of the "server" directory from the local filesystem
# to the "server" directory
# The "server" directory will be created inside the container within the project directory
# if it doesn't already exist

ADD ./server /app/server

# Starting the server

ENTRYPOINT ["venv/bin/python", "main.py"]
