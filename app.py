from faker import Faker

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, SmallInteger, BigInteger

from flask import Flask, render_template, \
    request, redirect, url_for, flash
import sqlite3
from forms import LoginForm, ContactForm, RegistrationForm, UserUpdateForm

app = Flask(__name__)

faker = Faker('ka_GE')


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# def add_user(first_name, last_name, email, age, password):
#     cursor.execute("""
#                 insert into users (first_name, last_name, email, age, password) values
#                 (?, ?, ?, ?, ?)
#                 """, (first_name, last_name, email, age, password))


# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"
# initialize the app with the extension
db.init_app(app)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    age: Mapped[int] = mapped_column(SmallInteger)
    address: Mapped[str]

#
# with app.app_context():
#     print('Creating Database and Models....')
#     db.create_all()
#     print('Created Tables....')


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
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            age = form.age.data
            password = form.password.data
            user = User.query.filter_by(first_name=first_name).first()
            user.first_name = 'sdas'

            if user is not None:
                flash('User With This Email Already Exists!')
                return render_template('register.html', form=form, user=user)

            users_list = []
            for _ in range(5):
                users_list.append(User(first_name=first_name + str(_), last_name=last_name + str(_),
                                       age=age + _, address='Tbilisi'))
            db.session.add_all(users_list)
            db.session.commit()
            flash('User Successfully Created!!')
            return redirect(url_for('home'))
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
    # cursor.execute("delete from users where id = ?", (user_id,))
    # flash('User Successfully Deleted!!!!!!!!!!!!!!!!!!!!!!!')
    # conn.commit()
    # close_connection(conn)
    return redirect(url_for('users'))
app.secret_key = 'ansdjasndjasjdnajsd9123n1'
if __name__ == '__main__':
    app.run(debug=True)
