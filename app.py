from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# DATABASE SETUP
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODEL (TABLE)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

# CREATE DATABASE
with app.app_context():
    db.create_all()

# HOME PAGE
@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

# ADD TASK
@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get("task")
    if task_text:
        new_task = Task(text=task_text)
        db.session.add(new_task)
        db.session.commit()
    return redirect('/')

# DELETE TASK
@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect('/')

# TOGGLE COMPLETE
@app.route('/complete/<int:id>')
def complete_task(id):
    task = Task.query.get(id)
    if task:
        task.done = not task.done
        db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)