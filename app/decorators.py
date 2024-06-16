from functools import wraps

from flask import session, redirect, url_for


def is_not_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return redirect(url_for('blog.home'))
        return func(*args, **kwargs)

    return wrapper


def is_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('user.login'))
        return func(*args, **kwargs)

    return wrapper
