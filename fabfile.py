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

def r():
    """Run app as is"""

    local('python manage.py -c dev.cfg run')
def sh():
    """Gimme that fancy script Shell
    """

    local('python manage.py --config dev.cfg shell')

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
