from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from . import auth
from .forms import LoginForm, RegistrationForm
from ..models import User
from .. import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    lform = LoginForm()
    if lform.validate_on_submit():
        user = User.query.filter_by(email = lform.email.data).first()
        if user is not None and user.verify_password(lform.password.data):
            login_user(user, lform.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password')
    return render_template('auth/login.html', form=lform)

#Add functionality for email confirmation email id change, password change, and password reset.
#Need to look into Flask email tools

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout sucessful')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    rform = RegistrationForm()
    if rform.validate_on_submit():
        user = User(email = rform.email.data,
                    username = rform.username.data,
                    password = rform.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration complete. You can now login')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=rform)
    
    