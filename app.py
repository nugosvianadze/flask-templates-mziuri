from faker import Faker
from random import randrange

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, SmallInteger, BigInteger, DateTime, Date

from flask import Flask, render_template, \
    request, redirect, url_for, flash
import sqlite3
import datetime
from forms import LoginForm, ContactForm, RegistrationForm, UserUpdateForm
from forms import PostForm

app = Flask(__name__)

faker = Faker('ka_GE')


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
# initialize the app with the extension
db.init_app(app)


user_roles_m2m = db.Table(
    "user_role",
    db.Column("user_id", db.ForeignKey('users.id'), primary_key=True),
    db.Column("role_id", db.ForeignKey('roles.id'), primary_key=True),
)


class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    age: Mapped[int] = mapped_column(SmallInteger)
    address: Mapped[str]
    id_card: Mapped['IdCard'] = db.relationship('IdCard', back_populates='user', uselist=False)
    roles = db.relationship('Role', secondary=user_roles_m2m, backref=db.backref('users', lazy='dynamic'))


class Post(db.Model):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str]
    image: Mapped[str]
    created_at = mapped_column(DateTime, default=datetime.datetime.now)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('User', backref='posts')


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


with app.app_context():
    print('Creating Database and Models....')
    db.create_all()
    print('Created Tables....')


def remove_spaces(value: str):
    return value.replace(' ', '')


def square(value):
    return int(value) ** 2


app.jinja_env.filters['remove_spaces'] = remove_spaces
app.jinja_env.filters['square'] = square


@app.route('/')
@app.route('/home')
def home():
    first_name, last_name = 'Nugoooo', 'Svianadze'
    title = 'Home Page'
    my_num = 25
    return render_template('index.html', first_name=first_name,
                           last_name=last_name, title=title)


@app.route('/features')
def features():
    title = 'fe atu r e s s'
    items = [1, 2, 3, 4, 5]
    my_num = 25
    return render_template('features.html', title=title, items=items,
                           my_num=my_num)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':

        if form.validate():
            print('forma validuria')
            return redirect(url_for('home'))
        print(form.errors)
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        print(form.validate_on_submit())
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            age = form.age.data
            password = form.password.data
            address = form.address.data
            user = User.query.filter_by(first_name=first_name).first()

            if user is not None:
                flash('User With This Email Already Exists!')
                return render_template('register.html', form=form, user=user)

            user = User(first_name=first_name, last_name=last_name,
                        age=age, address=address)
            db.session.add(user)
            db.session.commit()
            flash('User Successfully Created!!')
            return redirect(url_for('home'))
        print(form.errors)
        return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@app.route('/users')
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


app.secret_key = 'ansdjasndjasjdnajsd9123n1'
if __name__ == '__main__':
    app.run(debug=True)
