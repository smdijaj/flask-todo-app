from flask import Flask,flash,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.secret_key='secretkey'
db = SQLAlchemy(app)
class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    task=db.Column(db.String(200))
    completed=db.Column(db.Boolean,default=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
with app.app_context():
    db.create_all()
@app.route('/')
def home():
    todos=Todo.query.all()

    return render_template('index.html',todos=todos)
@app.route('/add',methods=['POST'])
def add():
    task=request.form.get('task')
    new_task=Todo(task=task)
    db.session.add(new_task)
    db.session.commit()
    flash('Task added successfully!')
    return redirect(url_for('home'))
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    flash('Task deleted successfully!')
    return redirect(url_for('home'))
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    task_to_edit = Todo.query.get(id)

    if request.method == 'POST':

        task_to_edit.task = request.form.get('task')

        db.session.commit()
        flash('Task updated successfully!')
        return redirect(url_for('home'))

    return render_template('edit.html', todo=task_to_edit)
@app.route('/complete/<int:id>')
def complete(id):
    task_to_complete=Todo.query.get(id)
    task_to_complete.completed=True
    db.session.commit()
    flash('Task marked as completed!')
    return redirect(url_for('home'))
@app.route('/completed')
def completed():
    todos = Todo.query.filter_by(completed=True).all()
    return render_template('index.html', todos=todos)
@app.route('/pending')
def pending():
    todos = Todo.query.filter_by(completed=False).all()
    return render_template('index.html', todos=todos)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
