from fabric.api import *
from fabric.colors import green, red
import time

env.project_name = 'civomega'
env.hosts = ['dev.civomega.com']
env.path = '/home/ubuntu/civomega_deploy'
env.user = 'ubuntu'
env.virtualhost_path = "/"


def setup():
    """
    Setup a fresh virtualenv as well as a few useful directories, then run
    a full deployment
    """
    require('hosts')
    require('path')
    #sudo('aptitude install -y nginx python-setuptools postgresql-client uwsgi uwsgi-plugin-python')
    #sudo('easy_install pip')
    #sudo('pip install virtualenv')

    # TODO: nginx config
    #sudo('cd /etc/apache2/sites-available/; a2dissite default;')

    run('mkdir -p %(path)s' % env)
    run('cd %(path)s; mkdir releases shared packages;' % env, warn_only=True)
    deploy()


def deploy():
    """
    Deploy the latest version of the site to the servers, install any
    required third party modules, install the virtual host and 
    then restart the webserver
    """
    require('hosts')
    require('path')
    env.release = time.strftime('%Y%m%d%H%M%S')

    upload_tar_from_git()
    bootstrap_venv()
    #install_site()
    symlink_current_release()
    migrate()
    restart_webserver()

def deploy_version(version):
    "Specify a specific version to be made live"
    require('hosts', provided_by=[local])
    require('path')
    env.version = version
    run('cd %(path)s; rm releases/previous; mv releases/current releases/previous;')
    run('cd %(path)s; ln -s $(version) releases/current')
    restart_webserver()

def rollback():
    """
    Limited rollback capability. Simple loads the previously current
    version of the code. Rolling back again will swap between the two.
    """
    require('hosts', provided_by=[local])
    require('path')
    run('cd %(path)s; mv releases/current releases/_previous;')
    run('cd %(path)s; mv releases/previous releases/current;')
    run('cd %(path)s; mv releases/_previous releases/previous;')
    restart_webserver()    


# Helpers. These are called by other functions rather than directly
def upload_tar_from_git():
    require('release', provided_by=[deploy, setup])
    "Create an archive from the current Git master branch and upload it"
    local('git archive --format=tar mtigas-deploy | gzip > %(release)s.tar.gz' % env)
    run('mkdir %(path)s/releases/%(release)s' % env)
    put('%(release)s.tar.gz' % env, '%(path)s/packages/' % env)
    run('cd %(path)s/releases/%(release)s && tar zxf ../../packages/%(release)s.tar.gz' % env)
    local('rm %(release)s.tar.gz' % env)
def bootstrap_venv():
    "Install the required packages from the requirements file using pip"
    require('release', provided_by=[deploy, setup])
    run('cd %(path)s/releases/%(release)s; virtualenv .; ./bin/pip install -M --download-cache %(path)s/packages -r requirements.txt' % env)
#def install_site():
#    "Add the virtualhost file to apache"
#    require('release', provided_by=[deploy, setup])
#    sudo('cd %(path)s/releases/%(release)s; cp $(project_name)$(virtualhost_path)$(project_name) /etc/apache2/sites-available/')
#    sudo('cd /etc/apache2/sites-available/; a2ensite $(project_name)') 
def symlink_current_release():
    "Symlink our current release"
    require('release', provided_by=[deploy, setup])
    run('cd %(path)s; rm releases/previous; mv releases/current releases/previous;' % env, warn_only=True)
    run('cd %(path)s; ln -s %(release)s releases/current' % env)
def migrate():
    "Update the database"
    require('project_name')
    run('cd %(path)s/releases/current/$(project_name); ./bin/python manage.py syncdb --migrate --noinput' % env)
def restart_webserver():
    "Restart the web server"
    sudo('kill -KILL `%(path)s/releases/previous/civomega.pid`' % env, warn_only=True)
    sudo('kill -KILL `%(path)s/releases/current/civomega.pid`' % env, warn_only=True)
    sudo('cd %(path)s/releases/current/$(project_name); uwsgi --ini uwsgi.ini' % env)
    sudo('service nginx reload' % env)
