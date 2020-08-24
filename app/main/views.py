from flask import render_template, session, redirect, url_for
from datetime import datetime
from . import main
from .forms import NameForm
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