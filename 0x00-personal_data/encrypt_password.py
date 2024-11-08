#!/usr/bin/env python3
''' hasp password encryption'''
import bcrypt


def hash_password(password: str) -> bytes:
    ''' takes the password and returns a salted hash
    password '''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    ''' validate if the provided password matches the hash password'''
    return bcrypt.checkpwd(password.encode('utf-8'), hashed_password)
