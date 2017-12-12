from flask_sqlalchemy import SQLAlchemy
from flask_security import RoleMixin, UserMixin

db = SQLAlchemy()
# Define models
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    orders = db.relationship('Orders', backref=db.backref('orders'))


class SuperSecureData(db.Model):
    __tablename__ = 'super_secure_data'

    id = db.Column(db.Integer, primary_key=True)
    credit_card_number = db.Column(db.String(255), unique=True)
    ssn = db.Column(db.String(255), unique=True)


class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item = db.Column(db.String(255))
    order_date = db.Column(db.DateTime())
