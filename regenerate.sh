#!/bin/bash

# For postgresql
echo "-> Remove clustr DB"
dropdb amigo
echo "-> Create clustr DB"
createdb amigo

echo "-> Run syncdb"
python manage.py migrate

echo "-> Load sample data"
python manage.py load_rsvp_replies
