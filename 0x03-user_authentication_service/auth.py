#!/usr/bin/env python3
''' a private method to hash password
takes in a str password and returns bytes'''
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    ''' takes a password and returns a salted bcrypt'''
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        ''' register a new user '''
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            pwd_hash = _hash_password(password)
            new_user = self._db.add_user(email, pwd_hash)
            return new_user
        raise ValueError('User {} already exists'.format(email))
