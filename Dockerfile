FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y build-essential libffi-dev
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
COPY . /app/