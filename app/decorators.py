from functools import wraps

from flask import session, redirect


def is_not_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return redirect('home')
        return func(*args, **kwargs)

    return wrapper


def is_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            return redirect('login')
        return func(*args, **kwargs)

    return wrapper
