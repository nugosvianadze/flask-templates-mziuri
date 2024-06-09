from faker import Faker
from random import randrange

import click
from functools import wraps

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, SmallInteger, BigInteger, DateTime, Date
from flask_migrate import Migrate

from flask import Flask, render_template, \
    request, redirect, url_for, flash, session
import sqlite3
import datetime

from werkzeug.utils import secure_filename

from forms import LoginForm, ContactForm, RegistrationForm, UserUpdateForm
from forms import PostForm
from enums import RoleEnum

app = Flask(__name__)

faker = Faker('ka_GE')


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate(render_as_batch=True)
admin = Admin(app, name='Mziuri', template_mode='bootstrap3')

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=1)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
# initialize the app with the extension
db.init_app(app)
migrate.init_app(app, db)


user_roles_m2m = db.Table(
    "user_role",
    db.Column("user_id", db.ForeignKey('users.id'), primary_key=True),
    db.Column("role_id", db.ForeignKey('roles.id'), primary_key=True),
)


@app.cli.command("create_roles")
def create_roles():
    roles = []
    for role in RoleEnum:
        roles.append(Role(title=role.value))
    db.session.add_all(roles)
    db.session.commit()
    click.echo('Role Successfully Created!!')


class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str]
    profile_picture: Mapped[str] = mapped_column(nullable=True)
    age: Mapped[int] = mapped_column(SmallInteger)
    address: Mapped[str]
    id_card: Mapped['IdCard'] = db.relationship('IdCard', back_populates='user', uselist=False)
    roles = db.relationship('Role', secondary=user_roles_m2m, backref=db.backref('users', lazy='dynamic'))
    posts = db.relationship('Post', backref='user', lazy='dynamic', cascade='all, delete')

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter_by(email=email, password=password).first()
        return user

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name


class Post(db.Model):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str]
    image: Mapped[str]
    created_at = mapped_column(DateTime, default=datetime.datetime.now)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'))


class IdCard(db.Model):
    __tablename__ = 'id_cards'
    id: Mapped[int] = mapped_column(primary_key=True)
    id_number: Mapped[int]
    created_at = mapped_column(DateTime)
    expire_at = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    user = db.relationship('User', back_populates='id_card')


class Role(db.Model):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

# with app.app_context():
#     print('Creating Database and Models....')
#     db.create_all()
#     print('Created Tables....')


class CustomModelView(ModelView):

    def is_accessible(self):
        if not session.get('user_id'):
            return False

        user_id = session.get('user_id')
        user = db.session.get(User, user_id)
        roles = [role.title for role in user.roles]
        if RoleEnum.ADMIN.value in roles:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


admin.add_view(CustomModelView(User, db.session))
admin.add_view(CustomModelView(Post, db.session))
admin.add_view(CustomModelView(IdCard, db.session))
admin.add_view(CustomModelView(Role, db.session))


def remove_spaces(value: str):
    return value.replace(' ', '')


def square(value):
    return int(value) ** 2


app.jinja_env.filters['remove_spaces'] = remove_spaces
app.jinja_env.filters['square'] = square


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


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route('/')
@app.route('/home')
@is_authenticated
def home():
    first_name, last_name = 'Nugoooo', 'Svianadze'
    title = 'Home Page'
    my_num = 25
    return render_template('index.html', first_name=first_name,
                           last_name=last_name, title=title)


@app.route('/features')
@is_authenticated
def features():
    title = 'fe atu r e s s'
    items = [1, 2, 3, 4, 5]
    my_num = 25
    return render_template('features.html', title=title, items=items,
                           my_num=my_num)


@app.route('/login', methods=['GET', 'POST'])
@is_not_authenticated
def login():
    form = LoginForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.authenticate(email, password)
            if not user:
                flash('Credentials Are Incorrect, Try Again!')
                return redirect('login')

            session['user_id'] = user.id
            session['username'] = user.full_name
            return redirect(url_for('home'))
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/register', methods=["POST", "GET"])
@is_not_authenticated
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        print(form.data)
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            age = form.age.data
            address = form.address.data
            form_roles = form.roles.data
            profile_picture = form.profile_picture.data

            filename = secure_filename(profile_picture.filename)
            profile_picture.save('static/uploads/' + filename)

            user = User.query.filter_by(first_name=first_name).first()

            db_roles = Role.query.filter(Role.title.in_(form_roles)).all()
            print(db_roles)
            if len(db_roles) != len(form_roles):
                flash('Some Roles Does Not Exsist!!!')
                return render_template('register.html', form=form, user=user)

            if user is not None:
                flash('User With This First Name Already Exists!')
                return render_template('register.html', form=form, user=user)

            user = User(first_name=first_name, last_name=last_name,
                        email=email, password=password,
                        age=age, address=address, profile_picture=filename)
            user.roles.extend(db_roles)
            db.session.add(user)
            db.session.commit()
            flash('User Successfully Created!!')
            return redirect(url_for('home'))
        print(form.errors)
        return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@app.route('/users')
@is_authenticated
def users():
    # stmt = db.select(User).where(User.age > 18).order_by(User.age)
    # user_data = db.session.execute(stmt).scalars().all()
    user_data = User.query.all()
    # user_data = db.session.query(User).where(User.age > 18).all()
    return render_template('users.html', users=user_data)


@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    form = UserUpdateForm()

    user = User.query.get(user_id)
    # user = db.get_or_404(User, user_id)
    if user is None:
        flash(f'User With ID={user_id} Does Not Exists!')
        return redirect(url_for('users'))
    if request.method == 'POST':
        first_name = form.first_name.data
        last_name = form.last_name.data
        age = form.age.data
        user.first_name = first_name
        user.last_name = last_name
        user.age = age
        db.session.commit()
        flash('User Successfuly Updated!')
        return redirect(url_for('update_user', user_id=user_id))
    return render_template('user_update.html', form=form, user=user)


@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):

    user = User.query.get(user_id)
    # user = db.get_or_404(User, user_id)
    if user is None:
        flash(f'User With ID={user_id} Does Not Exists!')
        return redirect(url_for('users'))

    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.first_name} Successfully Deleted!!')
    return redirect(url_for('users'))


@app.route('/user-posts/<int:user_id>')
def user_posts(user_id):
    user = User.query.get(user_id)
    if not user:
        flash(f'User With ID={user_id} Does Not Exists!')
        return redirect(url_for('users'))
    posts = user.posts
    return render_template('posts.html', posts=posts, user_id=user_id)


@app.route('/create_posts/<int:user_id>', methods=['GET', 'POST'])
def create_post(user_id):
    form = PostForm()
    user = User.query.get(user_id)
    if not user:
        flash(f'User With ID={user_id} Does Not Exists!')
        return redirect(url_for('users'))

    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            post = Post(title=title, content=content, image='image.png')
            user.posts.append(post)
            db.session.add(post)
            db.session.commit()
            flash('Post Successfuly Added')
            return redirect(url_for('user_posts', user_id=user_id))
        return render_template('create_post.html', form=form)

    return render_template('create_post.html', form=form, user_id=user_id)


@app.route('/create-id-card/<int:user_id>')
def create_id(user_id):
    user = User.query.get(user_id)
    if not user:
        flash(f'User With ID={user_id} Does Not Exists!')
        return redirect(url_for('users'))
    if user.id_card:
        flash(
            'That User ALready Has Id Card'
        )
        return redirect(url_for('users'))
    id_card = IdCard(id_number=randrange(10000, 32000), created_at=datetime.datetime(2024, 5, 5, 0, 0, 0),
                     expire_at=datetime.datetime(2027, 5, 5, 0, 0, 0), user=user)
    db.session.add(id_card)
    db.session.commit()
    flash('id card successfully created for user ', user.first_name)
    return redirect(url_for('users'))


@app.route('/add_roles')
def add_roles():
    user_role = Role(title='User')
    admin_role = Role(title='Admin')
    db.session.add_all([user_role, admin_role])
    db.session.commit()
    flash(f'roles {user_role.title} and {admin_role.title} successfully created!')
    return redirect(url_for('users'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Succussfully Logged Out')
    return redirect('login')


app.secret_key = 'ansdjasndjasjdnajsd9123n1'
if __name__ == '__main__':
    app.run(debug=True)
