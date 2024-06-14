from flask import Flask
from app.extensions import migrate, db
from app.filters import remove_spaces, square
from app.blog.models import Post, IdCard, Role
from app.user.models import User
from app.config import Config
from app.user.views import user_bp
from app.blog.views import blog_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    register_extensions(app)
    register_blueprints(app)
    register_filters(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    bps = [user_bp, blog_bp]
    for bp in bps:
        app.register_blueprint(bp)


def register_filters(app):
    app.jinja_env.filters['remove_spaces'] = remove_spaces
    app.jinja_env.filters['square'] = square
