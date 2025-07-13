# FHIRMD

A modern full-stack web application built with Django, featuring a robust backend API and dynamic frontend interface.

## Features

Backend: Django REST Framework API
Frontend: Django templates with modern JavaScript
Database: PostgreSQL (configurable)
Authentication: Django's built-in user authentication
Containerization: Docker and Docker Compose support
Python Version: 3.13.5

## Prerequisites

Docker
Git

## Install dependencies

pip install -r requirements.txt

## Running application locally

Build and run with Docker
docker-compose up --build

OR

python manage.py runserver

## Access the application locally

Frontend: http://localhost:8000
Admin Panel: http://localhost:8000/admin

## Project Structure

project/
├── FHIRMD/ # Django application
│ ├── settings.py # Base setup for the django application
│ ├── views.py # View functions/classes that the app will read from
├── frontend/ # Django raw html, no javascript
│ ├── models/ # holds basic classes and hardcoded data
│ ├── static/ # Static files (CSS, JS, images)
│ ├── views/ # Endspoint functions that then feed into appropriate template
│ ├── templates/ # Served HTML returned to the user from the relavant view/endpoint
├── requirements.txt # Python dependencies
├── Dockerfile # Docker configuration
├── docker-compose.yml # Docker Compose configuration
├── .env.example # Environment variables template
└── manage.py # Django management script
