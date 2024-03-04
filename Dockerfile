FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Run tests
RUN python manage.py test

# Copy static files
COPY staticfiles . /staticfiles/

# Create nginx user and group
RUN groupadd -r nginx && useradd -r -g nginx nginx

# Change ownership to nginx
RUN chown -R nginx:nginx . /staticfiles/

# Install Git
RUN apt-get update && apt-get install -y git

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]