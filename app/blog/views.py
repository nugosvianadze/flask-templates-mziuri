import datetime
from random import randrange

from flask import Blueprint, request, flash, redirect, session, url_for, render_template

import os

from app.blog.forms import PostForm
from app.decorators import is_authenticated
from app.extensions import db
from app.user.models import User
from app.blog.models import Role, Post, IdCard

base_templates = os.path.abspath('app/templates')
print(base_templates)
blog_bp = Blueprint('blog', __name__, template_folder=base_templates, url_prefix='/blog')


@blog_bp.route('/')
@blog_bp.route('/home')
@is_authenticated
def home():
    first_name, last_name = 'Nugoooo', 'Svianadze'
    title = 'Home Page'
    my_num = 25
    return render_template('blog/index.html', first_name=first_name,
                           last_name=last_name, title=title)


@blog_bp.route('/features')
@is_authenticated
def features():
    title = 'fe atu r e s s'
    items = [1, 2, 3, 4, 5]
    my_num = 25
    return render_template('blog/features.html', title=title, items=items,
                           my_num=my_num)


@blog_bp.route('/create_posts/<int:user_id>', methods=['GET', 'POST'])
def create_post(user_id):
    form = PostForm()
    user = User.query.get(user_id)
    if not user:
        flash(f'User With ID={user_id} Does Not Exists!')
        return redirect(url_for('user.users'))

    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            post = Post(title=title, content=content, image='image.png')
            user.posts.append(post)
            db.session.add(post)
            db.session.commit()
            flash('Post Successfuly Added')
            return redirect(url_for('user.user_posts', user_id=user_id))
        return render_template('blog/create_post.html', form=form)

    return render_template('blog/create_post.html', form=form, user_id=user_id)


@blog_bp.route('/create-id-card/<int:user_id>')
def create_id(user_id):
    user = User.query.get(user_id)
    if not user:
        flash(f'User With ID={user_id} Does Not Exists!')
        return redirect(url_for('user.users'))
    if user.id_card:
        flash(
            'That User ALready Has Id Card'
        )
        return redirect(url_for('user.users'))
    id_card = IdCard(id_number=randrange(10000, 32000), created_at=datetime.datetime(2024, 5, 5, 0, 0, 0),
                     expire_at=datetime.datetime(2027, 5, 5, 0, 0, 0), user=user)
    db.session.add(id_card)
    db.session.commit()
    flash('id card successfully created for user ', user.first_name)
    return redirect(url_for('user.users'))


@blog_bp.route('/add_roles')
def add_roles():
    user_role = Role(title='User')
    admin_role = Role(title='Admin')
    db.session.add_all([user_role, admin_role])
    db.session.commit()
    flash(f'roles {user_role.title} and {admin_role.title} successfully created!')
    return redirect(url_for('user.users'))
