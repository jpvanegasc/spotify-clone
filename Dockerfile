# pull the official docker image
FROM python:3.9.4-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY Pipfile Pipfile.lock ./
RUN pip3 install pipenv && pipenv install --system

# copy project
COPY . .

# run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]