from sqlalchemy import SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db


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