#! venv/bin/python3
# -*- coding: UTF-8 -*-


from app import create_app, db
from app.models import Product

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app('default')

manager = Manager(app)
migrate = Migrate(app, db)


def get_shell_context():
    return dict(app=app, db=db, Product=Product)


manager.add_command('shell', Shell(make_context=get_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
