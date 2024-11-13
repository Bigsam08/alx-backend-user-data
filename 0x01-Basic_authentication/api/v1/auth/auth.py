#!/usr/bin/env python3
''' '''
from flask import request
from typing import List, TypeVar


class Auth:
    ''' Authentication class for user'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' Public method for authentication'''
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        if not path.endswith('/'):
            path += '/'

        for exclude_path in excluded_paths:
            if exclude_path.endswith('/') and path == exclude_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        ''' authorization header'''
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        ''' return None'''
        return None
