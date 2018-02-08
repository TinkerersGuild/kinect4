from flask import Flask

app = Flask(__name__)
stuff = list()

from app import routes
