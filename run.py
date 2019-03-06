from bottle import run
from app import app

run(app=app, debug=True, reloader=True)
