from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)
class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    task=db.Column(db.String(200))
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
    return redirect(url_for('home'))
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    task_to_edit = Todo.query.get(id)

    if request.method == 'POST':

        task_to_edit.task = request.form.get('task')

        db.session.commit()

        return redirect(url_for('home'))

    return render_template('edit.html', todo=task_to_edit)@app.rout
if __name__ == '__main__':
    app.run(debug=True)