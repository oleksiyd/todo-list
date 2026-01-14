from flask import Blueprint, current_app, request, redirect, url_for, render_template, abort
import logging
from ..forms.todo_form import TodoForm
from ..forms.list_options_form import ListOptionsForm

todo_bp = Blueprint("todo", __name__)
logger = logging.getLogger(__name__)

@todo_bp.get("/")
def index():
    # Filter/sort GET form (no CSRF)
    list_options_form = ListOptionsForm(request.args)
    invalid = False

    if not list_options_form.validate():
        invalid = True
        list_options_form.set_defaults()

    todos = current_app.todo_service.list_filtered(list_options_form.to_model())
    return render_template(
        "index.html",
        todos=todos,
        list_options_form=list_options_form,
        invalid=invalid,
    )

@todo_bp.route("/add", methods=["GET", "POST"])
def add():
    todo_form = TodoForm()
    if todo_form.validate_on_submit():
        current_app.todo_service.add(todo_form.to_model())
        return redirect(url_for("todo.index"))
    return render_template("add.html", form=todo_form)

@todo_bp.get("/view/<int:todo_id>")
def view(todo_id: int):
    try:
        todo = current_app.todo_service.get(todo_id)
    except KeyError:
        abort(404)
    return render_template("view.html", todo=todo)

@todo_bp.route("/update/<int:todo_id>", methods=["GET", "POST"])
def update(todo_id: int):
    try:
        todo = current_app.todo_service.get(todo_id)
    except KeyError:
        abort(404)

    todo_form = TodoForm()

    # Pre-fill on GET
    if request.method == "GET":
        todo_form.process(obj=todo)

    if todo_form.validate_on_submit():
        current_app.todo_service.update(todo_form.to_model(todo_id))
        return redirect(url_for("todo.view", todo_id=todo_id))

    return render_template("update.html", form=todo_form, todo=todo)

@todo_bp.get("/complete/<int:todo_id>")
def complete(todo_id: int):
    try:
        current_app.todo_service.set_completed(todo_id, True)
    except KeyError:
        abort(404)
    return redirect(url_for("todo.index"))

@todo_bp.get("/incomplete/<int:todo_id>")
def incomplete(todo_id: int):
    try:
        current_app.todo_service.set_completed(todo_id, False)
    except KeyError:
        abort(404)
    return redirect(url_for("todo.index"))

@todo_bp.get("/delete/<int:todo_id>")
def delete(todo_id: int):
    try:
        current_app.todo_service.delete(todo_id)
    except KeyError:
        abort(404)
    return redirect(url_for("todo.index"))
