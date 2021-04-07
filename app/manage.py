from flask import Flask
import os
import sys
import logging
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + os.sep + '..')
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app.main import create_app


app = create_app('dev')


app.app_context().push()
manager = Manager(app)


@manager.command
def run():

    app.run(port=80)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
