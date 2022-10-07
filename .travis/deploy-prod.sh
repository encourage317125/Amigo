#!/bin/sh

if [[ $TRAVIS_BRANCH == 'prod' ]]; then
  echo "Host web1.amigoapp.co
    StrictHostKeyChecking no
    HostName 54.146.150.126
    User ubuntu
    ForwardAgent yes
    Identityfile ~/.ssh/id_rsa"	> ~/.ssh/config
	cat ~/.ssh/config
else
	echo "Not prod branch"
fi
