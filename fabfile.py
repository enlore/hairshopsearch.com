from fabric.api import *

project = 'hairshopsearch'

env.user = 'no'
env.hosts = ['demo.hairshopsearch.com']

def reset():
    """Reset local dev environment"""

    local('python manage.py init_db')

def d():
    """Run app in dev"""

    reset()
    local('python manage.py -c dev.cfg run')

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
