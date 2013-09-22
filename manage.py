from flask.ext.script import Manager, Server, Shell
from hairshopsearch.factory import create_app

m = Manager(create_app)

m.add_command('run', Server(port='9016'))

if __name__ == '__main__':
    m.run()
