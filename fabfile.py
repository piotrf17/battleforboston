from fabric.api import *

# Hosts to deploy onto.
env.hosts = ['battlef6@battleforboston.com']

env.project_root = '/home8/battlef6/mysite'

def prepare_deploy():
  local('python manage.py test tourny')
  local('git add -p && git commit')
  local('git push')

def deploy():
  with cd(env.project_root):
    run('git pull --no-edit')
    run('python manage.py migrate tourny')
    run('python manage.py collectstatic -v0 --noinput')
    run('touch /home8/battlef6/django.fcgi')
