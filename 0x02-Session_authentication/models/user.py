#!/usr/bin/env python3
''' User model '''
from models.base import Base
import hashlib


class User(Base):
    ''' User class base model'''

    def __init__(self, *args: list, **kwargs: dict):
        ''' class init user instance'''
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self._password = kwargs.get('_password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    @property
    def password(self) -> str:
        ''' get password and set to private property'''
        return self._password

    @password.setter
    def password(self, passwd: str):
        ''' set new password with encryption'''
        if passwd is None or type(passwd) is not str:
            self._password = None
        self._password = hashlib.sha256(passwd.encode()).hexdigest().lower()

    def is_valid_password(self, passwd: str) -> bool:
        ''' check if the password is a valid one'''
        if passwd is None or type(passwd) is not str:
            return False
        if self.password is None:
            return False
        encoded_pas = passwd.encode()
        return hashlib.sha256(encoded_pas).hexdigest().lower() == self.password

    def display_name(self) -> str:
        ''' display user name'''
        if self.email is None and self.first_name is None \
                and self.last_name is None:
            return ""
        if self.first_name is None and self.last_name is None:
            return f'{self.email}'
        if self.first_name is None:
            return '{}'.format(self.last_name)
        if self.last_name is None:
            return "{}".format(self.first_name)
        return "{} {}".format(self.first_name, self.last_name)
