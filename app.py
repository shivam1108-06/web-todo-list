from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        task_name = request.form["task"]

        new_task = Task(name=task_name)

        db.session.add(new_task)
        db.session.commit()

        return redirect("/")

    tasks = Task.query.all()

    return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):

    task = Task.query.get(id)

    db.session.delete(task)
    db.session.commit()

    return redirect("/")


@app.route("/complete/<int:id>")
def complete(id):

    task = Task.query.get(id)

    task.completed = True

    db.session.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)