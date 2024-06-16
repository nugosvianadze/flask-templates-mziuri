import os

from flask import Blueprint, request, flash, redirect, session, url_for, render_template
from werkzeug.utils import secure_filename
from .forms import LoginForm, RegistrationForm, UserUpdateForm

from app.extensions import db
from app.user.models import User
from app.blog.models import Role
from app.decorators import is_not_authenticated, is_authenticated

base_templates = os.path.abspath('app/templates')
print(base_templates)
user_bp = Blueprint('user', __name__, template_folder=base_templates, url_prefix='/user')

"""localhost:5000/user/login"""
@user_bp.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('blog.home'))
        return render_template('user/login.html', form=form, base_templates=base_templates)
    return render_template('user/login.html', form=form, base_templates=base_templates)


@user_bp.route('/register', methods=["POST", "GET"])
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
                return render_template('user/register.html', form=form, user=user)

            if user is not None:
                flash('User With This First Name Already Exists!')
                return render_template('user/register.html', form=form, user=user)

            user = User(first_name=first_name, last_name=last_name,
                        email=email, password=password,
                        age=age, address=address, profile_picture=filename)
            user.roles.extend(db_roles)
            db.session.add(user)
            db.session.commit()
            flash('User Successfully Created!!')
            return redirect(url_for('blog.home'))
        print(form.errors)
        return render_template('user/register.html', form=form)
    return render_template('user/register.html', form=form)


@user_bp.route('/users')
@is_authenticated
def users():
    # stmt = db.select(User).where(User.age > 18).order_by(User.age)
    # user_data = db.session.execute(stmt).scalars().all()
    user_data = User.query.all()
    # user_data = db.session.query(User).where(User.age > 18).all()
    return render_template('users.html', users=user_data)


@user_bp.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    form = UserUpdateForm()

    user = User.query.get(user_id)
    # user = db.get_or_404(User, user_id)
    if user is None:
        flash(f'User With ID={user_id} Does Not Exists!')
        return redirect(url_for('user.users'))
    if request.method == 'POST':
        first_name = form.first_name.data
        last_name = form.last_name.data
        age = form.age.data
        user.first_name = first_name
        user.last_name = last_name
        user.age = age
        db.session.commit()
        flash('User Successfuly Updated!')
        return redirect(url_for('user.update_user', user_id=user_id))
    return render_template('user/user_update.html', form=form, user=user)


@user_bp.route('/delete_user/<int:user_id>')
def delete_user(user_id):

    user = User.query.get(user_id)
    # user = db.get_or_404(User, user_id)
    if user is None:
        flash(f'User With ID={user_id} Does Not Exists!')
        return redirect(url_for('user.users'))

    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.first_name} Successfully Deleted!!')
    return redirect(url_for('user.users'))


@user_bp.route('/user-posts/<int:user_id>')
def user_posts(user_id):
    user = User.query.get(user_id)
    if not user:
        flash(f'User With ID={user_id} Does Not Exists!')
        return redirect(url_for('user.users'))
    posts = user.posts
    return render_template('user/posts.html', posts=posts, user_id=user_id)


@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Succussfully Logged Out')
    return redirect(url_for('user.login'))
