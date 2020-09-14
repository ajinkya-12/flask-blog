from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

#Dtabase table for Role
class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    user = db.relationship('User', backref='user_role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role,self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return '<Role: {}, Permission: {}, Default: {}>'.format(self.name, self.permissions, self.default)

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permission(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm #Using bitwise operator as permissions are powers of two,
        #Check if bit exists

    #We need to run this function to add roles to database. To run Role.insert_role()
    @staticmethod
    def insert_role():
        roles = {
            'User' : [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator' : [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'Administrator' : [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE,
            Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name = r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for p in roles[r]:
                role.add_permission(p)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

#Database table for User
class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.user_role is None:
            if self.email == current_app.config['APP_ADMIN']:
                self.user_role = Role.query.filter_by(name = 'Administrator').first()
            if self.user_role is None:
                self.user_role = Role.query.filter_by(default = True).first()

    def can(self, perm):
        return (self.user_role is not None) and (self.user_role.has_permission(perm))

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}, Role: {}>'.format(self.username, self.user_role)

class AnonymousUser(AnonymousUserMixin):
    def can(self, perm):
        return False
    
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

from app import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))