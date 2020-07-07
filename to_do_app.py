import os
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)



app.config['SECRET_KEY'] = 'myseckey'


basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)




class ListItem(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Text)
    done = db.Column(db.Boolean)



@app.route('/')
def index():
    allitems = ListItem.query.all()
    return render_template('index.html', allitems=allitems)

@app.route('/add', methods=['POST'])
def add():
    addnew = ListItem(item=request.form['additem'], done=False)
    db.session.add(addnew)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/done/<num>')
def done(num):
    doneitem = ListItem.query.get(num)
    if doneitem.done ==False:
        doneitem.done = True
    else:
        doneitem.done =False
    db.session.commit()

    return redirect('/')


@app.route('/remove/<num>')
def remove(num):
    removeitem=ListItem.query.get(num)
    db.session.delete(removeitem)
    db.session.commit()

    return redirect('/')








if __name__ == '__main__':
    app.run(debug=True)
