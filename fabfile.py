from fabric.api import *

project = 'Hair Shop Search'

env.user = "no"
env.hosts = [""]

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
    """Run app in debug"""

    reset()
    local("python manage.py init_db")
    local("python manage.py run")

def pack():
    local("python setup.py sdist --formats=gztar")

def deploy():
    pass
