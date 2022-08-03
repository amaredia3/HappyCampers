# README

## Introduction

Currently, every National Park has its own unique way to handle visitors’ needs. This makes it challenging for people to plan trips. Having a system where reservations, park attractions, park reviews and many other items can be accessed together will save time for the visitors and help prevent potential oversights in their itinerary. Furthermore, consolidating all this information for all national parks into one resource will help people identify the best park for them. ​

[Happy Campers HandBook](https://happycampers310.herokuapp.com/) is a central web site that allows you to view, make reservations at, and rate many of the [US National Parks](https://en.wikipedia.org/wiki/List_of_national_parks_of_the_United_States).

## To run locally

### Requirements

- Python
- django
- Bootstrap
- Heroku
- PostgreSQL

### External dependencies

- Heroku CLI
- Git
- GitHub

## Run

Clone the repo:

`git clone https://github.com/Summer22-CSCE-310-Database-Systems/HappyCampers_Team04_Sprint1.git`



To set up locally, install contents from requirements.txt using (python -m pip install -r requirements.txt)

Add (SECRET_KEY= "*") to settings.py

To run: python manage.py migrate
        python manage.py runserver
        
For windows, in Procfile replace $PORT with %PORT%

