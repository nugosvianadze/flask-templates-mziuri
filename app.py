from sqlite3 import Cursor
from faker import Faker

from flask import Flask, render_template, \
    request, redirect, url_for, flash
import sqlite3
from forms import LoginForm, ContactForm, RegistrationForm

app = Flask(__name__)

faker = Faker('ka_GE')


def add_user(first_name, last_name, email, age, password):
    cursor.execute("""
                insert into users (first_name, last_name, email, age, password) values 
                (?, ?, ?, ?, ?)
                """, (first_name, last_name, email, age, password))
# cursor.execute("""create table if not exists users
#             (id integer primary key,
#             first_name text,
#             last_name text,
#             age integer,
#             email text,
#             password text)""")
# conn.commit()
#
# cursor.execute("""
#                 create table if not exists laptops
#                 (id integer primary key,
#                 model text,
#                 brand text,
#                 year integer,
#                 color text,
#                 size real)
#                 """
#                )
# conn.commit()


# conn.close()
# cursor.close()


def create_connection():
    conn = sqlite3.connect('sqlite.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def create_cursor(conn):
    return conn.cursor()



# conn = create_connection()
# cursor = create_cursor(conn)
# for _ in range(30):
#     add_user(faker.first_name(), faker.last_name(), faker.email(), 20, faker.password())
# conn.commit()
# conn.close()

def remove_spaces(value: str):
    return value.replace(' ', '')


def square(value):
    return int(value) ** 2


app.jinja_env.filters['remove_spaces'] = remove_spaces
app.jinja_env.filters['square'] = square


@app.route('/')
@app.route('/home')
def home():
    first_name, last_name = 'Nugo', 'Svianadze'
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
            conn = create_connection()
            cursor = create_cursor(conn)
            cursor.execute("""
            select * from users where email = ?
            """, (email,))
            user_exists = cursor.fetchone()
            conn.close()
            if user_exists is not None:
                flash('User With This Email Already Exists!')
                return render_template('register.html', form=form, user=user_exists)
            conn = create_connection()
            cursor = create_cursor(conn)
            cursor.execute("""
            insert into users (first_name, last_name, email, age, password) values 
            (?, ?, ?, ?, ?)
            """, (first_name, last_name, email, age, password))
            conn.commit()
            conn.close()
            flash('User Successfully Created!!')
            return redirect(url_for('home'))
        return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@app.route('/users')
def users():
    conn = create_connection()
    cursor = create_cursor(conn)
    cursor.execute("""
    select * from users
    """)
    users = cursor.fetchall()
    return render_template('users.html', users=users)


app.secret_key = 'ansdjasndjasjdnajsd9123n1'
if __name__ == '__main__':
    app.run(debug=True)
