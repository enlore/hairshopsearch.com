#!/home/no/.venvs/hairshopsearch/bin/python
from flask.ext.script import Manager, Server, Shell 
from hairshopsearch.factory import create_app

m = Manager(create_app)

def _make_context():
    return dict(
           app=create_app(),
            )

m.add_command('run', Server(port='9016'))
m.add_command('shell', Shell(make_context=_make_context))

if __name__ == '__main__':
    m.run()
