# Pulling the base image

FROM python:3.11

# Setting root directory of the application

WORKDIR /app

# Copying requirements file from the local filesystem

COPY ./requirements.txt /app/requirements.txt

# Creating and activating virtual environment, then installing dependencies

#RUN python3 -m venv venv && \
#    /bin/bash -c "source venv/bin/activate && \
#    pip install --no-cache-dir --upgrade -r /app/requirements.txt"

RUN python3 -m venv venv && \
    /bin/bash -c ". venv/bin/activate && \
    pip install --no-cache-dir --upgrade -r /app/requirements.txt"

# Copying main from the local filesystem

COPY ./main.py /app/main.py

RUN mkdir /app/server

COPY ./server /app/server

RUN pip freeze

# Starting the server

ENTRYPOINT ["venv/bin/python", "main.py"]
