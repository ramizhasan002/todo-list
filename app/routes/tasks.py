from flask import Blueprint, render_template, redirect, url_for, request, flash
from datetime import datetime
from flask_login import login_required, current_user
from app.form import EmptyForm
from app.models import Task, TaskStatus
from app.extensions import db

tasks_bp = Blueprint("tasks", __name__)

def get_task(task_id):
    return Task.query.filter_by(
        id=task_id,
        user_id=current_user.id
    ).first()

# HOME
@tasks_bp.route("/")
@login_required
def home():
    form = EmptyForm()
    active_tasks = Task.query.filter(
        Task.user_id == current_user.id,
        Task.is_deleted.is_(False),
        Task.status != TaskStatus.COMPLETED
    ).all()

    completed_tasks = Task.query.filter(
        Task.user_id == current_user.id,
        Task.is_deleted.is_(False),
        Task.status == TaskStatus.COMPLETED
    ).all()

    return render_template("home.html", form=form, active_tasks = active_tasks, completed_tasks = completed_tasks)


# ADD TASK 
@tasks_bp.route("/task/add", methods=["POST"])
@login_required
def add_task():
    title = request.form.get("title", '').strip()
    description = request.form.get("description", '').strip()
    time_date = request.form.get("time_date", '').strip()


    if not title:
        flash('Please enter a task title', 'error')
        return redirect(url_for('tasks.home'))
    
    if len(title) > 100:
        flash('Title must be under 100 characters', 'error')
        return redirect(url_for('tasks.home'))
    
    if len(description) > 500:
        flash('Description must be under 500 characters', 'error')
        return redirect(url_for('tasks.home'))

    verified_date = None
    if time_date:
        try:
            verified_date = datetime.strptime(time_date, '%Y-%m-%dT%H:%M')
        except ValueError: 
            flash('Invalid date and time', 'error')
            return redirect(url_for('tasks.home'))
        
    new_task = Task(
        title=title,
        description=description or None,
        time_date=verified_date,
        status = TaskStatus.PENDING,
        is_deleted = False,
        user_id = current_user.id
    )

    try:
        db.session.add(new_task)
        db.session.commit()
        flash('Task added!', 'success')
        return redirect(url_for('tasks.home'))
    
    except Exception:
        db.session.rollback()
        flash("Something went wrong. Please try again.", "error")
        return redirect(url_for("tasks.home"))

    
        

# Edit 
@tasks_bp.route("/task/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    form = EmptyForm()

    task = get_task(task_id)
    
    if not task:
        flash("No task found", "error")
        return redirect(url_for("tasks.home"))
    
    if request.method == "POST":
        title = request.form.get("title", '').strip()
        description = request.form.get("description", '').strip()
        time_date = request.form.get("time_date", '').strip()

        if not title:
            flash('Please enter a task title', 'error')
            return redirect(url_for('tasks.edit_task', task_id=task.id))
        
        if len(title) > 100:
            flash('Title must be under 100 characters', 'error')
            return redirect(url_for('tasks.edit_task', task_id=task.id))
        
        if len(description) > 500:
            flash('Description must be under 500 characters', 'error')
            return redirect(url_for('tasks.edit_task', task_id=task.id))

        verified_date = None
        if time_date:
            try:
                verified_date = datetime.strptime(time_date, '%Y-%m-%dT%H:%M')

            except ValueError: 
                flash('Invalid date and time', 'error')
                return redirect(url_for('tasks.edit_task', task_id=task.id))
        

        task.title = title
        task.description = description or None
        task.time_date = verified_date or task.created_at

        try:
            db.session.commit()
            flash("Task saved", "success")
            return redirect(url_for('tasks.home'))
        
        except Exception:
            db.session.rollback()
            flash("Something went wrong. Please try again.", "error")
            return redirect(url_for("tasks.edit_task"))

    return render_template("edit.html", form=form, task=task)


# Recycle
@tasks_bp.route("/recycle-bin")
@login_required
def recycle_bin():
    deleted_tasks = Task.query.filter(
        Task.user_id == current_user.id,
        Task.is_deleted.is_(True)
    ).all()
    return render_template("recycle.html", deleted_tasks=deleted_tasks)


# Restore
@tasks_bp.route("/task/<int:task_id>/restore", methods=["POST"])
@login_required
def restore_task(task_id):
    task = get_task(task_id)
 
    if not task:
        flash("No task found", "error")
        return redirect(url_for("tasks.home"))
    
    task.is_deleted = False
    db.session.commit()
    flash("Task restored", "success")
    return redirect(url_for("tasks.recycle_bin")) 


# Empty Bin
@tasks_bp.route("/empty-bin", methods=["POST"])
@login_required
def empty_bin():
    deleted_count = Task.query.filter(
        Task.user_id == current_user.id,
        Task.is_deleted.is_(True)
    ).delete()

    db.session.commit()

    flash(f"Permanently deleted ({deleted_count})", "error")
    return redirect(url_for("tasks.recycle_bin"))


# COMPLETE TASK
@tasks_bp.route("/task/<int:task_id>/complete", methods=["POST"])
@login_required
def complete_task(task_id):
    task = get_task(task_id)

    if not task:
        flash("No task found", "error")
        return redirect(url_for("tasks.home"))
    
    task.status = TaskStatus.COMPLETED
    db.session.commit()
    return redirect(url_for("tasks.home"))
    

# UNCOMPLETE TASK
@tasks_bp.route("/task/<int:task_id>/uncomplete", methods=["POST"])
@login_required
def uncomplete_task(task_id):
    task = get_task(task_id)

    if not task:
        flash("No task found", "error")
        return redirect(url_for("tasks.home"))
    
    task.status = TaskStatus.PENDING
    db.session.commit()
    return redirect(url_for("tasks.home", section="completed"))



# Delete 
@tasks_bp.route("/task/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):
    task = get_task(task_id)
 
    if not task:
        flash("No task found", "error")
        return redirect(url_for("tasks.home"))
    
    task.is_deleted = True
    db.session.commit()
    flash("Moved to Recycle Bin", "info")

    source = request.form.get("source")
    if source == "completed_tasks":
        return redirect(url_for("tasks.home", section="completed"))
    
    return redirect(url_for("tasks.home"))



# Delete Permanently
@tasks_bp.route("/task/<int:task_id>/delete-permanently", methods=["POST"])
@login_required
def delete_permanently(task_id):
    task = get_task(task_id)

    if not task:
        flash("No task found", "error")
        return redirect(url_for("tasks.home"))
    
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted permanently", "error")

    next_page = request.form.get("next_page")
    if next_page == "recycle_bin":
        return redirect(url_for("tasks.recycle_bin"))
    
    return redirect(url_for("tasks.home", section="completed"))

    

# Delete all task
@tasks_bp.route("/task/delete-all-tasks", methods=["POST"])
@login_required
def delete_all_tasks():
    deleted_count = Task.query.filter(
        Task.user_id == current_user.id,
        Task.is_deleted.is_(False),
        Task.status != TaskStatus.COMPLETED
    ).update({
        Task.is_deleted: True
    })

    if deleted_count == 0:
        flash("No task found", "error")
        return redirect(url_for("tasks.home"))
    
    elif deleted_count == 1:
        db.session.commit()
        flash("Task moved to recycle bin", "info")
        return redirect(url_for("tasks.home"))
    
    else:
        db.session.commit()
        flash("All tasks moved to recycle bin", "info")
        return redirect(url_for("tasks.home"))
    
