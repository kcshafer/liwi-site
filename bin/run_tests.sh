#!/bin/bash

createdb 'liwi_test'
python manage.py syncdb --database='liwi_test'
mkdir mail
python manage.py test
rm -rf mail/
dropdb 'liwi_test'