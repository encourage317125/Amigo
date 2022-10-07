Build status: [![Build Status](https://travis-ci.com/JoinAmigo/amigo-web.svg?token=mqzQUzfs8sg4XGmA9aUn&branch=master)](https://travis-ci.com/JoinAmigo/amigo-web) on [master](https://github.com/JoinAmigo/amigo-web/tree/master)
[![Build Status](https://travis-ci.com/JoinAmigo/amigo-web.svg?token=mqzQUzfs8sg4XGmA9aUn&branch=master)](https://travis-ci.com/JoinAmigo/amigo-web) on [prod](https://github.com/JoinAmigo/amigo-web/tree/prod)

# Amigo API

[Amigo documentation](http://joinamigo.github.io/amigo-web/), refer [Update Documentation](https://github.com/JoinAmigo/amigo-web/#update-documentation) section below to learn how to update it.

## Getting up and running

###Verify xcode command line tools:

```xcode-select -p```

should show ```/Applications/Xcode.app/Contents/Developer```

###Install HomeBrew - The missing package manager for OS X:
 
   * Install homebrew from https://brew.sh by running the following command:
   * `ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
   * Verify homebrew is up to date
   * `brew update`
   * Verify homebrew has no issues
   * `brew doctor`

###Install required HomeBrew packages

```
brew bundle
```

should output success like:

```
Succeeded in tapping homebrew/bundle
Succeeded in installing openssl
Succeeded in installing python
Succeeded in installing postgresql
Succeeded in installing redis
Succeeded in installing phantomjs

Success: 6 Fail: 0
```

Note you might need to install Python via homebrew with open ssl

```
brew install python --with-brewed-openssl
```

###Install Python packages

```
pip install --upgrade pip setuptools
pip install fabric
pip install redis
pip install postgres
pip install virtualenv
pip install -r requirements/development.txt
```

###Prepare a local machine for development:

`fab init`

###Setup your server environment:

- Get the heroku config by running: `heroku config -s -a amigo-master`
- edit local `.env` file contaning project secrets, that are not part of the Source Code:
It should have these values:

```
DJANGO_SECRET_KEY="Secret_Key_Created_by_Fab_Init"
DATABASE_URL="postgres://localhost/amigo"
TWILIO_ACCOUNT_SID="ACc64a86f188d5f0218a524650aadfa6ac"
TWILIO_AUTH_TOKEN="b134efe9ec64ba8615e65887fa6f95ee"
TWILIO_PHONE_NUMBER="+18472644624"
USERVOICE_SUBDOMAIN_NAME="joinamigo"
USERVOICE_API_KEY="V0zo5bsSu55k1Hz8g127DA"
USERVOICE_API_SECRET="quUFMz9blvpRk0Jrh0Dp3QFo5iSxR73XMdArAfx37qw"
```
Add the following values:

```
DEBUG=True
DJANGO_DEBUG=True
DJANGO_ENVIRONMENT=[Dev]
DJANGO_CONFIGURATION=Development
ZEROPUSH_AUTH_TOKEN=Value_From_Heroku_Config
DJANGO_SETTINGS_MODULE=settings.development
DJANGO_SITE_DOMAIN=localhost:8000

```

###Start local server with all required services (redis,postgres)
```
fab honcho
```

#### To start services separately
Start Postgres

```
postgres -D /usr/local/var/postgres
```

Stop Postgres

`pg_ctl stop -D /usr/local/var/postgres -m fast`

Start redis

```
redis-server /usr/local/etc/redis.conf
```

To start local server run:

`fab serve` - start django server on [http://localhost:8000/](http://localhost:8000/)

To kill server:

`kill -9 $(lsof -ti tcp:8000)`

###To verify that cloned code run tests:

`fab test` - run the local server tests

###Create local administrator

`fab manage:createsuperuser` - create local admin for [http://localhost:8000/admin](http://localhost:8000/admin)

 - email: `alldev@amigo.io`
 - phone number: `+1 415-555-1111`
 - password: `amigo` insecure password for only local development server

###Development tools

####Load DJango development shell:

`fab shell`

####Update Documentation

`fab serve_docs`
This will run a local HTTP server and as you are editing \*.md files you can instantly view your changes at: `127.0.0.1:8001` (Read [mkdocs](http://www.mkdocs.org/) to learn more).

`fab deploy_docs`
This will update server documentation on github pages: [http://joinamigo.github.io/amigo-web/](http://joinamigo.github.io/amigo-web/):

####List available fabric tasks:

`fab list`

#### Heroku commands

Clone existing heroku app

```heroku git:clone -a amigo-master```

Show heroku configuration

```heroku config -s -a amigo-master```

Create Administrator:

`heroku run python manage.py createsuperuser --app amigo-master`

__TODO:__ find out why `heroku run fab createsuperuser --app amigo-master` does not work

Load `.env` variables to your current shell

```export $(cat .env | xargs)```

## Contributing

Golden Rule:

> Anything in **master** is always **deployable**.

Avoid working on `master` branch, create a new branch with meaningful name, send pull request asap. Be vocal!

Refer to [CONTRIBUTING.md][contributing]

[contributing]: http://github.com/JoinAmigo/amigo-web/tree/master/CONTRIBUTING.md

##Production deployment:
```shell
git checkout master
fab test
bumpversion release
bumpversion --no-tag patch # 'patch' can be replaced with 'minor' or 'major'
git push origin master
git push origin master --tags
git checkout prod
git rebase master
git push origin prod
```

For deploying to production:

Edit your local ` ~/.ssh/config` to have correct hostname from AWS:

```
Host web1.amigoapp.co
    HostName ec2-54-80-0-153.compute-1.amazonaws.com
    User ubuntu
    ForwardAgent yes
    Identityfile ~/.ssh/id_aws
```

Then run:

```shell
git checkout prod
git rebase master
fab prod configure
```
You may experience errors during inital setup because the environment variables are not set.  Just create a `.env` file in the `amigo-web folder`.  Also, if ngnix is not starting type `sudo service nginx restart` to reload your page with redirects in place.

When updating production ensure your static files are hosted in the [S3 com-amigo bucket](https://console.aws.amazon.com/s3/home?bucket=com-amigo), and they are made publicly accesssible, i.e. [https://com-amigo.s3.amazonaws.com/css/normalize.css](https://com-amigo.s3.amazonaws.com/css/normalize.css)

`gunicorn --pythonpath="$PWD" wsgi:application` - restart the django server
`kill -9 $(lsof -ti tcp:8000)` - kill a process on a port, such as port 8000.
