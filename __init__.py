from flask import *

application = Flask(__name__)
application.config.from_object('config')


