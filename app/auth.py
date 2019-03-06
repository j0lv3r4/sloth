from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature
from passlib.hash import bcrypt
from sqlalchemy import exists

from app.models import User
from config import SECRET


class AuthException(Exception):
    pass


def generate_auth_token(payload, expiration=3600):
    serializer = TimedJSONWebSignatureSerializer(SECRET, expires_in=expiration)
    return serializer.dumps(payload).decode("utf-8")


def verify_auth_token(token):
    serializer = TimedJSONWebSignatureSerializer(SECRET)
    try:
        data = serializer.loads(token)
    except SignatureExpired:
        raise AuthException("Token is expired.")
    except BadSignature:
        raise AuthException("Token is invalid.")
    return data


def user_exists(username, db_session):
    return db_session.query(exists().where(User.username == username)).scalar()


def sign_up(username, password, private_key, public_key, db_session):
    user = User(
        username=username,
        password=bcrypt.hash(password),
        private_key=private_key,
        public_key=public_key,
    )

    db_session.add(user)
    db_session.commit()

    return {
        "auth_token": str(generate_auth_token(user.id)),
        "username": user.username,
        "user_id": user.id,
    }
