from app import create_app
from app.enums import RoleEnum
from app.blog.models import Role
from app.extensions import db

import click


app = create_app()


@app.cli.command("create_roles")
def create_roles():
    roles = []
    for role in RoleEnum:
        roles.append(Role(title=role.value))
    db.session.add_all(roles)
    db.session.commit()
    click.echo('Role Successfully Created!!')
