from fabric.api import *

project = 'Hair Shop Search'

env.user = "no"
env.hosts = ["hairshopsearch.com"]

def setup():
    """Set up venv"""

    local("virtualenv venv")
    activate_this = "venv/bin/activate_this.py"
    execfile(activate_this, dict(__file__=activate_this))
    local("python setup.py install")
    reset()

def reset():
    """Reset local dev environment"""

    local("python manage.py init_db")

def d():
    """Run app in dev"""

    reset()
    local("python manage.py -c dev.cfg run")

def pack():
    local("python setup.py sdist --formats=gztar")

def deploy():
    pass
