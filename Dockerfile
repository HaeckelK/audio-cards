FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
COPY /app .

RUN pip install -r requirements.txt

ENV BUILD_ENV=DEV
CMD ["flask", "run", "--host=0.0.0.0"]