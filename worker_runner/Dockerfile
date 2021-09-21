FROM python:3.9.4-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y python3-dev gcc libc-dev libffi-dev
RUN apt-get -y install libpq-dev gcc 

# install dependencies
COPY worker_runner/requirements.txt .
RUN pip install --upgrade pip
# copy project
COPY worker_runner/. .
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
