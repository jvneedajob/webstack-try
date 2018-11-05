from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from __init__ import app
from exts import db
from model import User ,Question,Answer
import os
import unittest
import config
import coverage


app.config.from_object(config)
manager = Manager(app)

migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)

@manager.command
def test():
    tests = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(branch=True, include='projectA/*')
    cov.start()
    tests = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary:')
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'coverage')
    cov.html_report(directory=covdir)
    cov.erase()


if __name__ == "__main__":
    manager.run()

