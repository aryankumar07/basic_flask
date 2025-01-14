from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# use this to create your own database in python shell instead of using db.create_all()
# $ python
# >>> from project import app, db
# >>> app.app_context().push()
# >>> db.create_all()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id  = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200),nullable=False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route("/", methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Somethting went wrong sorry'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks = tasks)
    

@app.route('/delete/<int:id>')
def delete_task(id):
    task = Todo.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return 'problem in deleting the task'
    

@app.route('/update/<int:id>',methods = ['POST','GET'])
def update_page(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        try:
            task.content = request.form['content']
            db.session.commit()
            return redirect('/')
        except:
            return "something went wrong in updating"
    else:
        return render_template('update.html',task = task)
        

if __name__=="__main__":
    app.run(debug=True)