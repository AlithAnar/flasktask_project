# -*- coding: utf-8 -*-
import datetime

from flask import flash, redirect, render_template, request, session, url_for, Blueprint
from project.views import login_required
from forms import AddTaskForm
from project.models import Task
from project import db

tasks_blueprint = Blueprint(
    'tasks', __name__,
    url_prefix='/tasks',
    template_folder='templates',
    static_folder='static'
)



@tasks_blueprint.route('/tasks/')
@login_required
def tasks():
    open_tasks = db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())
    closed_tasks = db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())
    return render_template('tasks.html', form=AddTaskForm(request.form), open_tasks=open_tasks,
                           closed_tasks=closed_tasks, username=session['name'])


@tasks_blueprint.route('/add/', methods=['POST'])
@login_required
def new_task():
    form = AddTaskForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_task = Task(form.name.data, form.due_date.data, form.priority.data, '1', session['user_id'],
                            datetime.datetime.now())
            db.session.add(new_task)
            db.session.commit()
            flash("New entry added succesfully")
            return redirect(url_for('tasks.tasks'))
        else:
            error = 'Not valid data in form!'
            return render_template('tasks.html', error=error, form=form)


@tasks_blueprint.route('/complete/<int:task_id>/',)
@login_required
def complete(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().user_id or session['role'] == "admin":
        task.update({"status": "0"})
        db.session.commit()
        flash("Task marked as complete")
        return redirect(url_for('tasks.tasks'))
    else:
        flash("Not permitted")
        return redirect(url_for('tasks.tasks'))


@tasks_blueprint.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().user_id or session['role'] == "admin":
        task.delete()
        db.session.commit()
        flash("Task deleted")
        return redirect(url_for('tasks.tasks'))
    else:
        flash("Not permitted")
        return redirect(url_for('tasks.tasks'))

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text, error), 'error')

