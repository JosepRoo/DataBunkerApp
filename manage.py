import os
from app import create_app
from flask_script import Manager
from flask import Flask

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
#app = Flask(__name__)

if __name__ == '__main__':
	manager.run()
