## Architecture

```sequence
iOS/\nClient->Web\nServer: API Request
Web\nServer-->Memcached: Cache
Memcached-->Web\nServer: 
Web\nServer->Postgres: Persistent Storage
Postgres->Web\nServer: 
Web\nServer-->Memcached: Update cache
Web\nServer-->SMTP(SES): Enqueue emails
Web\nServer-->Twilio: Enqueue SMS
Web\nServer-->ZeroPush\nService: Enqueue push notifications
Web\nServer->iOS/\nClient: API Response
SMTP(SES)->iOS/\nClient: Email
ZeroPush\nService->iOS/\nClient: Push notification
Twilio->iOS/\nClient: SMS
Note over Web\nServer: Django Framework
```

## Deploying Project

The deployment are managed via travis, but for the first time you'll need to set the configuration values on each of the server. Read this only, if you need to deploy for the first time.

### Heroku

Run these commands to deploy a new project to Heroku:

```
heroku create amigo-<ENV_NAME_HERE> --buildpack https://github.com/heroku/heroku-buildpack-python
heroku addons:create heroku-postgresql:dev --app=amigo-<ENV_NAME_HERE>
heroku addons:create pgbackups:auto-month --app=amigo-<ENV_NAME_HERE>
heroku addons:create sendgrid:starter --app=amigo-<ENV_NAME_HERE>
heroku addons:create memcachier:dev --app=amigo-<ENV_NAME_HERE>
heroku pg:promote DATABASE_URL --app=amigo-<ENV_NAME_HERE>

heroku config:set DJANGO_CONFIGURATION=Production --app=amigo-<ENV_NAME_HERE>
heroku config:set DJANGO_SECRET_KEY=`openssl rand -base64 32` --app=amigo-<ENV_NAME_HERE>
heroku config:set DJANGO_AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID --app=amigo-<ENV_NAME_HERE>
heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY --app=amigo-<ENV_NAME_HERE>
heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME=amigo-<ENV_NAME_HERE> --app=amigo-<ENV_NAME_HERE>
heroku config:set TWILIO_ACCOUNT_SID=TWILIO_ACCOUNT_SID_HERE --app=amigo-<ENV_NAME_HERE>
heroku config:set TWILIO_AUTH_TOKEN=TWILIO_AUTH_TOKEN_HERE --app=amigo-<ENV_NAME_HERE>
heroku config:set TWILIO_PHONE_NUMBER=TWILIO_PHONE_NUMBER_HERE --app=amigo-<ENV_NAME_HERE>
heroku config:set TWILIO_CALLBACK_DOMAIN=APPLICATION_HOST_DOMAIN_HERE --app=amigo-<ENV_NAME_HERE>
heroku config:set AMIGO_APPSTORE_URL=AMIGO_APPSTORE_URL_HERE --app=amigo-<ENV_NAME_HERE>
heroku config:set DJANGO_SITE_DOMAIN=DJANGO_SITE_DOMAIN_HERE --app=amigo-<ENV_NAME_HERE>
heroku config:set DJANGO_SITE_SCHEME=DJANGO_SITE_SCHEME_HERE --app=amigo-<ENV_NAME_HERE>
heroku config:set DJANGO_SITE_NAME=DJANGO_SITE_NAME_HERE --app=amigo-<ENV_NAME_HERE>

heroku addons:create redistogo --app=amigo-<ENV_NAME_HERE>
heroku addons:create redismonitor --url `heroku config:get REDISTOGO_URL --app=amigo-<ENV_NAME_HERE>` --app=amigo-<ENV_NAME_HERE>


heroku addons:add zeropush:inception --app=amigo-<ENV_NAME_HERE>
heroku config:set ZEROPUSH_AUTH_TOKEN=`heroku config:get ZEROPUSH_DEV_TOKEN --app=amigo-<ENV_NAME_HERE>` --app=amigo-<ENV_NAME_HERE>

heroku config:set MIXPANEL_PROJECT_TOKEN=<MIXPANEL_PROJECT_TOKEN_HERE> --app=amigo-<ENV_NAME_HERE>

heroku addons:create scheduler:standard --app=amigo-<ENV_NAME_HERE>

git remote <ENV_NAME_HERE> git@heroku.com:amigo-<ENV_NAME_HERE>.git
git push <ENV_NAME_HERE> master 
heroku run python manage.py migrate --app=amigo-<ENV_NAME_HERE>
heroku run python manage.py createsuperuser --app=amigo-<ENV_NAME_HERE>
heroku run python manage.py load_rsvp_replies --app=amigo-<ENV_NAME_HERE>
heroku open --app=amigo-<ENV_NAME_HERE>
```

## Further Reading

For setting up zero push with heroku: https://devcenter.heroku.com/articles/zeropush

**NOTE:**

Open the heroku scheduler[1] or cron of less than 1hr, with following command:

    python manage.py send_event_reminders

[1] `heroku addons:open scheduler --app=amigo-master`

For production, use the following config:

```
heroku config:set ZEROPUSH_AUTH_TOKEN=`heroku config:get ZEROPUSH_PROD_TOKEN --app=amigo-<ENV_NAME_HERE>` --app=amigo-<ENV_NAME_HERE>
```

### AWS

# RDS

TODO

# EC2
For deploying on aws you need to configure all the addons provided and use python-dotenv to store and read enironment variables.

```
Host web1.amigoapp.co
    hostname ec2-54-80-0-153.compute-1.amazonaws.com
    user ubuntu
    ForwardAgent yes
    identityfile PATH_OF_REMOTE_SERVER_PRIVATE_KEY
```

Add your github private key to your local ssh-agent, which will be used by ansible on remote server to fetch the code using `ForwardAgent`

    ssh-add PATH_TO_YOUR_GITHUB_PRIVATE_KEY

Make sure you have the latest code pushed to github in the branch `prod`.

```
fab prod config:set,DJANGO_CONFIGURATION,Production
fab prod config:set,DATABASE_URL=RDS_URL


Run the following commond to deploy to server:

    fab prod configure

```
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
<script src="//bramp.github.io/js-sequence-diagrams/raphael-min.js"></script>
<script src="//bramp.github.io/js-sequence-diagrams/underscore-min.js"></script>
<script src="//bramp.github.io/js-sequence-diagrams/sequence-diagram-min.js"></script>
<script src="//bramp.github.io/js-sequence-diagrams/svginnerhtml.min.js"></script>
<script>
    $('.sequence').sequenceDiagram({"theme": "simple"}).parent().removeClass("prettyprint").css({"background-color": "#fff", "text-align": "center"});
</script>
