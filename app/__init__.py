import os
import json
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from bottle import (
    Bottle,
    get,
    post,
    request,
    static_file,
    template,
    TEMPLATE_PATH,
    redirect,
    response,
    error,
    abort,
)
from bottle.ext import sqlalchemy
from app.config import DOMAIN
from app.models import engine, Base, User
from app.utils import create_key_pair, get_webfinger
from app.auth import sign_up

app = Bottle()

# Plugins
sqlalchemy_plugin = sqlalchemy.Plugin(engine, Base.metadata, keyword="db", create=True)

app.install(sqlalchemy_plugin)

PROJECT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH.insert(0, "{0}/templates".format(PROJECT_PATH))


def post_get(name, default=""):
    return request.POST.get(name, default).strip()


@app.get("/")
def home():
    return {"message": "hello world"}


@app.post("/auth/signup")
def post_signup(db):
    username = post_get("username")
    password = post_get("password")
    private_key, public_key = create_key_pair()

    # https://stackoverflow.com/a/32463880/1869996
    try:
        user = sign_up(username, password, private_key, public_key, db)
        response["status_code"] = 201
        return user
    except IntegrityError as err:
        abort(409, "Username already taken")
    except SQLAlchemyError as err:
        abort(500, err)


@app.get("/u/<username>/.well-known/webfinger")
def webfinger(username):
    response.content_type = "application/json"
    return get_webfinger(username, DOMAIN)


@app.post("/u/<username>/inbox")
def post_inbox(username, db):
    try:
        # 1. Look for user
        # 2. Insert post in database with user asociation
        # 3. Return 201
        user = db.query(User).filter_by(username=username).first()
    except NoResultFound as err:
        print("User not found: {0}".format(err))
    except SQLAlchemyError as err:
        print(err)


@error(404)
def error404(err):
    print(err)
    return "Nothing here, sorry"


@error(500)
def error500(err):
    return "Something's wrong. {0}".format(err)

