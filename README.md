# README

## Introduction

Currently, every National Park has its own unique way to handle visitors’ needs. This makes it challenging for people to plan trips. Having a system where reservations, park attractions, park reviews and many other items can be accessed together will save time for the visitors and help prevent potential oversights in their itinerary. Furthermore, consolidating all this information for all national parks into one resource will help people identify the best park for them. ​

[Happy Campers HandBook](https://happycampers310.herokuapp.com/) is a central web site that allows you to view, make reservations at, and rate many of the [US National Parks](https://en.wikipedia.org/wiki/List_of_national_parks_of_the_United_States).

## Requirements ##

This code has been run and tested on:

python=3
Django=4.0.6
django-on-heroku=1.1.2
Bootstrap=5
postgres=14.4

## Installation

To download, clone the repo: `git clone https://github.com/Summer22-CSCE-310-Database-Systems/HappyCampers_Team04_Sprint1.git`

## Testing

Input testing is handled with proper error handling through exceptions. No unit tests were needed.

## To run locally

Install dependecies from requirements.txt (python -m pip install -r requirements.txt)
For windows, in Procfile replace $PORT with %PORT%

## To excute code and view website

After installing dependencies from requirements.txt, Run: python manage.py runserver

### Requirements

- Python
- django (see version in requirements.txt)
- Bootstrap
- Heroku
- PostgreSQL(14.4) when running locally the app should connect to our prod DB automatically. No local DB setup is required.

### External dependencies

- Heroku CLI (optional)
- Git
- GitHub
- Python
- Pip

## Deployment ##

No deployment setup required. App is already deployed to Heroku (https://happycampers310.herokuapp.com)

## CI/CD ##

For CI/CD we set Heroku to automatically deploy our main branch. Any time code is merged into main, Heroku re-deploys and app is updated.

## References ## 

Hosting Django on Heroku: https://realpython.com/django-hosting-on-heroku/

## Support ##

Admins and Users looking for help/support with the app should contact the developers who contributed to this repository.

