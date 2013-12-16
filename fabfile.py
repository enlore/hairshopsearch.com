from fabric.api import *
import os

project = 'hairshopsearch'

env.user = 'no'
env.hosts = ['demo.hairshopsearch.com']

def t():
    """Run tha tests
    """

    local('nosetests')

def reset():
    """Reset local dev environment"""

    local('python manage.py reset_db')

def rebuild_index(filename):
    local('python manage.py reset_index provider')
    local('python manage.py reset_db')
    local('python manage.py mock_from_csv {}'.format(filename))

def d(filename):
    """Run app in dev"""

    rebuild_index(filename)
    local('python manage.py run')

def r():
    """Run app as is"""

    instance = os.path.join(os.getcwd(), 'instance')
    local('python manage.py -i {} run'.format(instance))

def sh():
    """Gimme that fancy script Shell
    """

    local('python manage.py --config dev.cfg shell')

def css():
    """Compile less to css
    """

    local('node_modules/recess/bin/recess app/static/css/main.less --compile\
        > app/static/css/main.css')

def tiny_css():
    """Compile and compress less
    """

    local('node_modules/recess/bin/recess app/static/css/main.less --compile\
        --compress > app/static/css/main.css')

def pack():
    local('python setup.py sdist --formats=gztar')

def deploy():
    dist = local('python setup.py --fullname', capture=True).strip()
    put('dist/%s.tar.gz' % dist, '/tmp/%s.tar.gz' % dist)
    with cd('/tmp'):
        run('tar xzf /tmp/%s.tar.gz' % dist)
        with cd('%s' % dist):
            run('/var/www/hss-proto/venv/bin/python setup.py install')

    run('rm -rf /tmp/%s.tar.gz /tmp/%s' % (dist, dist))

    local('tar czvf static.tar.gz app/static/')
    put('static.tar.gz', '/tmp/static.tar.gz')
    with cd('/var/www/hss-proto'):
        run('tar xzvf /tmp/static.tar.gz')
