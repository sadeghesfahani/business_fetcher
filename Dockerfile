FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /opt/services/app/src

COPY . .

COPY environments/production.env .env

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --no-input
