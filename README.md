bc2
===

What's done:
- Rosters and Govboard
- Half of polls

What needs to be done:
- Add a model for Faculty Fellows in rosters/model.py - easy
- Add a model for reslife in rosters/model.py - easy 
- Finish implementation of multiple choice polls - medium
- Finish implementation of ranked choice polls - hard
- Make a reservation system - medium

Quick Start
==

1. Install [Django 1.6](https://docs.djangoproject.com/en/dev/releases/1.6/)
2. `git clone http://github.com/MisterAbc/bc2
3. `python manage.py syncdb`
4. Ask zl4ry@virginia.edu for a brown college roster, save it in the same directory, call it `roster.csv`
5. `python manage.py update_roster roster.csv`
6. `python manage.py runserver`
7. Go to [localhost:8000](localhost:8000)
8. There's something about making an admin account, use Django documentation to learn more!
