
<img src="https://www.djangoproject.com/m/img/badges/djangopowered126x54.gif" border="0" alt="Powered by Django." title="Powered by Django." />



************************************************
***********READ ME - IMPORTANT******************

* This is a application in state to be deployed to a production server. This means that it includes sensitive information including:
    * server keys
    * password
    * secure server and application urls
    * database schemas
    * security information
    * confidential business processes

* In order to ensure security of our users, proprietary information the following rules must be kept in regards to the contents of this repository and any future repositories belonging to LiWi Inc.

* Only authorized employees will have access to this repository, this includes executives and members of the development staff. Access to source code is on a need only basis. In order to maintain security, access will be granted on a need only basis. 
* Contractors dealing with direct development responsibilities will be granted access to the code on an as needed basis, and will be granted access via a github user of there own. 
* Access by users should always be done through properly registered GitHub accounts, no access should at any time be granted through other channels.
* Cloning, interactions with the contents of this repository should ONLY EVER take place on your private computer, never access this repository and/or especially clone it's contents on a public machine AT ANY TIME.
* No part of this repository should at any time be published, uploaded or distributed via any public manner. This includes public repositories, message boards, forums or other manners. 
* If at any time contents of this repository is distributed via a public manner, it is critical that it be addressed and removed immediatly, and that the lead developer be notified so that proper action be taken to maintain security.

FOR ANY QUESTIONS, ISSUES OR PROBLEMS CONTACT:

KC Shafer
Lead Engineer
kclshafer@gmail.com


************************************************
************************************************

===============

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
