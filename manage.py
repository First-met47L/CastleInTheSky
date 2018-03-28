import os
from application import db,create_app
from application.models import User,Role
from flask_script import Manager,Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app=app)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)

manager.add_command("shell",Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()