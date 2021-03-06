
from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

#config variables
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#db model
class Todo_List(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    done = db.Column(db.Boolean)

    

@app.route('/')
def index():
    #show all todos
    todo= Todo_List.query.all()
    return render_template('base.html',todo=todo)



@app.route('/add',methods=["POST"])
def add():
    # add todo task
    title = request.form.get("title")
    new_todo = Todo_List(title = title,done = False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route('/view/<int:todo_id>')
def view(todo_id):
    # view todo task
    todo = Todo_List.query.filter_by(id=todo_id).first()
    # todo.done = not todo.done
    db.session.commit()
    return render_template("view.html",todo=todo)


@app.route('/mark/<int:todo_id>')
def mark(todo_id):
    # mark todo task as read    
    todo = Todo_List.query.all()
    mytodo = Todo_List.query.filter_by(id=todo_id).first()
    mytodo.done = not mytodo.done
    db.session.commit()
    return render_template("base.html",mytodo=todo,todo=todo)


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    # view todo task
    todo = Todo_List.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route('/complete',methods=["GET"])
def complete():
    # filter done and not done
    todo = Todo_List.query.filter_by(done=True).all()
    print(todo)
    return render_template("base.html",todo=todo)


@app.route('/incomplete',methods=["GET"])
def incomplete():
    # filter done and not done
    todo = Todo_List.query.filter_by(done=False).all()
    print(todo)
    return render_template("base.html",todo=todo)

@app.route('/')
def back():
    return redirect(url_for("index"))



if __name__ == "__main__":

    #create the database
    db.create_all()

    # new_todo = Todo_List(title="Todo-1",done=False)
    # db.session.add(new_todo)
    # db.session.commit()

    app.run(debug = True)
    






