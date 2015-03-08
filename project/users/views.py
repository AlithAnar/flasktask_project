# -*- coding: utf-8 -*-

from flask import flash, redirect, render_template, request, session, url_for, Blueprint
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError
from project.views import login_required
from project.models import User
from project import db, bcrypt


users_blueprint = Blueprint(
    'users', __name__,
    url_prefix ='/users',
    template_folder='templates',
    static_folder='static'
)



@users_blueprint.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('role', None)
    session.pop('name', None)
    flash("You have been logged out!")
    return redirect(url_for('users.login'))


@users_blueprint.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            u = User.query.filter_by(name=request.form['name']).first()
            if u is None:
                error = 'Invalid credentials'
                return render_template('login.html', form=form, error=error)
            elif bcrypt.check_password_hash(u.password, request.form['password']):
                session['logged_in'] = True
                session['user_id'] = u.id
                session['role'] = u.role
                session['name'] = u.name
                flash("Legged in successfully")
                return redirect(url_for('tasks.tasks'))
        else:
            error = 'not valid data in form'
            return render_template('login.html', form=form, error=error)
    if request.method == 'GET':
        return render_template('login.html', form=form, error=error)

@users_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(form.name.data,
                            form.email.data,
                            bcrypt.generate_password_hash(form.password.data))
                            # form.password.data)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Thanks for registering')
                return redirect(url_for('users.login'))
            except IntegrityError:
                error = 'already taken'
                return render_template('register.html', form=form, error=error)
        else:
            error = 'Not valid data in form!'
            return render_template('register.html', form=form, error=error)
    if request.method == 'GET':
        return render_template('register.html', form=form)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text, error), 'error')

