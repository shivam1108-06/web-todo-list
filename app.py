from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ------------------
# Database Model
# ------------------

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(20), default="Medium")
    due_date = db.Column(db.String(20))


# ------------------
# Create Database
# ------------------

with app.app_context():
    db.create_all()


# ------------------
# Home Page
# ------------------

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        task_name = request.form["task"]
        priority = request.form["priority"]
        due_date = request.form["due_date"]

        new_task = Task(
            name=task_name,
            priority=priority,
            due_date=due_date
        )

        db.session.add(new_task)
        db.session.commit()

        return redirect("/")

    search = request.args.get("search")
    filter_type = request.args.get("filter")

    tasks = Task.query

    if search:
        tasks = tasks.filter(
            Task.name.contains(search)
        )

    if filter_type == "completed":
        tasks = tasks.filter_by(completed=True)

    elif filter_type == "pending":
        tasks = tasks.filter_by(completed=False)

    tasks = tasks.all()

    total_tasks = Task.query.count()

    completed_tasks = Task.query.filter_by(
        completed=True
    ).count()

    pending_tasks = Task.query.filter_by(
        completed=False
    ).count()

    return render_template(
        "index.html",
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks
)


# ------------------
# Delete Task
# ------------------

@app.route("/delete/<int:id>")
def delete(id):

    task = Task.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return redirect("/")


# ------------------
# Complete Task
# ------------------

@app.route("/complete/<int:id>")
def complete(id):

    task = Task.query.get_or_404(id)

    task.completed = True

    db.session.commit()

    return redirect("/")


# ------------------
# Edit Task
# ------------------

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    task = Task.query.get_or_404(id)

    if request.method == "POST":
        task.name = request.form["task"]
        db.session.commit()

        return redirect("/")

    return render_template(
        "edit.html",
        task=task
    )


if __name__ == "__main__":
    app.run(debug=True)