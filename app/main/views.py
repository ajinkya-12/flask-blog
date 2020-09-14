from flask import render_template, session, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_moment import Moment
from datetime import datetime
from . import main
from .forms import NameForm, EditProfileForm
from .. import db 
from ..models import User #Not defined

@main.route('/', methods=['GET', 'POST'])
def index():
    nform = NameForm()
    if nform.validate_on_submit():
        user = User.query.filter_by(username=nform.name.data).first()
        if user is None:
            user = User(username=nform.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = nform.name.data
        nform.name.data = ''
        return redirect(url_for('main.index'))
    return render_template('index.html', form=nform, name=session.get('name'),
                            known=session.get('known', False), current_time = datetime.utcnow())

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    return render_template('user.html', user=user)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    eform = EditProfileForm()
    if eform.validate_on_submit():
        current_user.username = eform.uname.data
        current_user.name = eform.name.data
        current_user.location = eform.location.data
        current_user.bio = eform.bio.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('main.user', username=current_user.username))
    eform.uname.data = current_user.username
    eform.name.data = current_user.name
    eform.location.data = current_user.location
    eform.bio.data = current_user.bio
    return render_template('edit_profile.html', form=eform)