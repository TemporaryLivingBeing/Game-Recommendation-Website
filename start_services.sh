#!/bin/bash

# Start contact application
/var/www/html/PersonalSite/Projects/GameRecommendationWebsite/myenv/bin/gunicorn --workers 3 --bind unix:contact.sock -m 007 app.wsgi:contact &

# Start recommendation application
/var/www/html/PersonalSite/Projects/GameRecommendationWebsite/myenv/bin/gunicorn --workers 3 --bind unix:rec.sock -m 007 app.wsgi:rec &

/var/www/html/PersonalSite/Projects/GameRecommendationWebsite/myenv/bin/gunicorn --workers 3 --bind unix:app.sock -m 007 app.wsgi:app &
# Wait for all background processes
wait
