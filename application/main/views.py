from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask_login import login_required,current_user
from . import main
from .forms import NameForm
from .. import db
from ..models import User



@main.route ('/index', methods=['GET', 'POST'])
def index():
    form = NameForm ()
    if form.validate_on_submit ():
        user = User.query.filter(User.username == form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        # form.name.data = ''
        return redirect (url_for ('.index')) #abbreviation of main.submit_page
        # return redirect (url_for ('main.index'))

    return render_template ('index.html', form=form, name=session.get ('name'), known = session.get('known', False),current_user=current_user)

@main.route('/secret')
@login_required
def secret():
    return 'Only authenticated user are allowed'