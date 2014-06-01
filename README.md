liwi-site
=========

Main Liwi Site - contained as single app 

================

Requirements 

- Python 2.7
- Django 1.6.5
- Postgresql

developer requirements

- homebrew
- pip 

================

How to setup 

================

1. install homebrew 
2. brew install postgresql
3. clone this repository
4. pip install -r requirements.txt
5. postgres -D /usr/local/var/postgres
6. python manage.py syncdb
7. python manage.py runserver
