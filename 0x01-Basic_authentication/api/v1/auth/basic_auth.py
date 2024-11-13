#!/usr/bin/env python3
''' Basic Auth'''
from api.v1.auth.auth import Auth
from typing import List, Tuple, TypeVar
import base64
from models.user import User


class BasicAuth(Auth):
    ''' Basic Auth class that inherites parent class'''

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        ''' '''
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        ''' decode auth header'''
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decode_bytes = base64.b64decode(base64_authorization_header)
            return decode_bytes.decode('utf-8')
        except Exception as e:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> Tuple[str, str]:  # type: ignore
        ''' users credentials '''
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):  # type: ignore
        ''' getting credentials'''
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})
        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        ''' retrive User instance for a request'''
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base_auth = self.extract_base64_authorization_header(auth_header)
        if base_auth is None:
            return None
        decode_auth = self.decode_base64_authorization_header(base_auth)
        if decode_auth is None:
            return None
        email, password = self.extract_user_credentials(decode_auth)
        if email is None or password is None:
            return None
        return self.user_object_from_credentials(email, password)
