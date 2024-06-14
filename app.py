from flask import session

from app import create_app

from app.extensions import db


app = create_app()


# with app.app_context():
#     print('Creating Database and Models....')
#     db.create_all()
#     print('Created Tables....')


@app.before_request
def make_session_permanent():
    session.permanent = True


if __name__ == '__main__':
    app.run(debug=True)
