from fabric.api import *
import os

project = 'hairshopsearch'

env.user = 'no'
env.hosts = ['demo.hairshopsearch.com']

def map():
    local("python manage.py dump_url_map | column -t -s '()'")

def t():
    """Run tha tests
    """

    local('py.test')

def reset():
    """Reset local dev environment"""

    instance = os.path.join(os.getcwd(), 'instance')
    local('python manage.py -i {} reset_db'.format(instance))

def rebuild_index(filename):
    local('python manage.py reset_index provider')
    local('python manage.py reset_db')
    local('python manage.py mock_from_csv {}'.format(filename))
<<<<<<< HEAD
    local('python manage.py populate_db')

=======
>>>>>>> fd620a4233836b188a76e7330ecd38a96d76dba0
def d(filename):
    """Run app in dev"""

    rebuild_index(filename)
    instance = os.path.join(os.getcwd(), 'instance')
    local('python manage.py -i {} run'.format(instance))

def r():
    """Run app as is"""

    instance = os.path.join(os.getcwd(), 'instance')
    local('python manage.py -i {} run'.format(instance))

def sh():
    """Gimme that fancy shell
    """

    local('python manage.py --config dev.cfg shell')

def css():
    """Compile less to css
    """

    local('node_modules/recess/bin/recess app/static/css/main.less --compile\
        > app/static/css/main.css')

def pack():
    local('python setup.py sdist --formats=gztar')

def deploy():
    dist = local('python setup.py --fullname', capture=True).strip()
    put('dist/%s.tar.gz' % dist, '/tmp/%s.tar.gz' % dist)
    with cd('/tmp'):
        run('tar xzf /tmp/%s.tar.gz' % dist)
        with cd('%s' % dist):
            run('/home/no/.virtualenvs/hss-app/bin/python setup.py install')

    run('rm -rf /tmp/%s.tar.gz /tmp/%s' % (dist, dist))

    # create instance folder
    # push production conf
    put('dist/config.py', '/var/www/hss-proto/instance')
    put('fabfile.py', '/var/www/hss-proto')
    put('manage.py', '/var/www/hss-proto')
