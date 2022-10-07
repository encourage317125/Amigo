# -*- coding: utf-8 -*-
# !/usr/bin/env python2
'''Fabric file for managing this project.

See: http://www.fabfile.org/
'''
from __future__ import unicode_literals, absolute_import, with_statement
import os
from os.path import join, isdir
from fabric.api import local, env, lcd, cd, prefix, run, sudo
from contextlib import contextmanager as _contextmanager

ROOT_DIR = os.getcwd()

env.project_name = 'amigo'
env.apps_dir = join(ROOT_DIR, env.project_name)
env.docs_dir = join(ROOT_DIR, 'docs')
env.virtualenv_dir = join(ROOT_DIR, 'venv')
env.dotenv_path = join(ROOT_DIR, '.env')
env.requirements_file = join(ROOT_DIR, 'requirements/development.txt')
env.shell = "/bin/bash -l -i -c"
env.use_ssh_config = True
env.config_setter = local

env.coverage_omit = '*tests*,*commands*,*migrations*,*admin*,*config*,*wsgi*'


# ==========================================================================
#  Enviroments
# ==========================================================================
def prod():
    env.host_group = 'production'
    env.remote = 'origin'
    env.branch = 'prod'
    env.hosts = ['web1.amigoapp.co']
    env.dotenv_path = '/home/ubuntu/amigo-web/.env'
    env.config_setter = run


def configure(tags=''):
    '''Setup a host using ansible scripts'''
    # local('git push')
    # env.host_group = 'production'
    cmd = 'ansible-playbook -i hosts site.yml --limit=%(host_group)s' % env
    with lcd('provisioner'):
        if tags:
            cmd += " --tags '%s'" % tags
        local(cmd)


def init(vagrant=False):
    '''Prepare a local machine for development.'''

    install_deps()
    config('set', 'DJANGO_SECRET_KEY', '`openssl rand -base64 32`')
    config('set', 'DATABASE_URL', 'postgres://localhost/%(project_name)s' % env)
    local('createdb %(project_name)s' % env)  # create postgres database
    manage('migrate')


def install_deps(file=env.requirements_file):
    '''Install project dependencies.'''
    verify_virtualenv()
    # activate virtualenv and install
    with virtualenv():
        local('pip install -r %s' % file)


def serve_docs():
    with lcd(ROOT_DIR):
        # create_graph_models()
        local('mkdocs serve')


def deploy():
    test()
    configure(tags='deploy')


def deploy_docs():
    with lcd(ROOT_DIR):
        # create_graph_models()
        local('mkdocs gh-deploy')
        local('rm -rf _docs_html')


def shell():
    manage('shell_plus')


def serve(host='127.0.0.1:8000'):
    '''Start an enhanced runserver'''
    install_deps()
    migrate()
    manage('runserver_plus %s' % host)


def makemigrations(app):
    '''Create new database migration for an app.'''
    manage('makemigrations %s' % app)


def migrate():
    '''Apply database migrations.'''
    manage('migrate')


def flush():
    manage('flush --noinput')


def honcho():
    '''Start development server with all it's dependencies
    '''
    local('honcho -f Procfile.dev start')


def stop():
    '''Stop development server with all it's dependencies
    '''
    env.PGDATA = '/usr/local/var/postgres'
    local('server_process=$(lsof -ti tcp:8000) && kill -9 $server_process || true')
    local('redis-cli SHUTDOWN || true')
    local('pg_ctl status && pg_ctl stop || true')


def test(options=''):  # --ipdb
    '''Run tests locally.'''
    with virtualenv():
        local('python2 -m flake8 .')
        local("coverage run --source=amigo --omit='%s' -m py.test %s" % (env.coverage_omit, options))
        local("coverage report -m")
        local('cd provisioner; ansible-playbook -i hosts site.yml --syntax-check')


def createapp(appname):
    '''fab createapp <appname>
    '''
    path = join(env.apps_dir, appname)
    local('mkdir %s' % path)
    manage('startapp %s %s' % (appname, path))


def config(action=None, key=None, value=None):
    '''Manage project configuration via .env

    see: https://github.com/theskumar/python-dotenv
    Usages: fab config:set,[key],[value]
    '''
    command = 'dotenv'
    command += ' -f %s ' % env.dotenv_path
    command += action + " " if action else " "
    command += key + " " if key else " "
    command += value if value else ""
    env.config_setter('touch %(dotenv_path)s' % env)

    if env.config_setter == local:
        with virtualenv():
            env.config_setter(command)
    else:
        env.config_setter(command)
        sudo('supervisorctl restart all')


# Helpers
# ------------------------------------------------------------------------------
def manage(cmd, venv=True):
    with virtualenv():
        local('python manage.py %s' % cmd)


def create_graph_models():
    graph_model_output = join(env.docs_dir, 'img/graph_model.svg')
    manage("graph_models -a -g -o %s" % graph_model_output)


@_contextmanager
def virtualenv():
    '''Activates virtualenv context for other commands to run inside it
    '''
    with cd(ROOT_DIR):
        with prefix('source %(virtualenv_dir)s/bin/activate' % env):
            yield


def verify_virtualenv():
    '''This modules check and install virtualenv if it not present.
    It also creates local virtualenv directory if it's not present
    '''
    from distutils import spawn
    if not spawn.find_executable('virtualenv'):
        local('sudo pip install virtualenv')

    if not isdir(env.virtualenv_dir):
        local('virtualenv %(virtualenv_dir)s' % env)


def load_sample_data(venv=True):
    ''' generate user and superuser '''
    with virtualenv():
        local('python manage.py runscript create_calvin_and_admin')
