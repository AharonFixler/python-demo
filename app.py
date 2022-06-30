from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

def contact():
    if request.method == 'POST':
        
    elif request.method == 'GET':
        return render_template('contact.html', form=form)
    
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Add Task':
            task_content = request.form['content']
            new_task = Todo(content=task_content)

            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your task'
            
        elif request.form['submit_button'] == 'Test DB':
            conn = psycopg2.connect(
                    host="ec2-52-22-136-117.compute-1.amazonaws.com",
                    database="d2f0gk8obcb2i7",
                    user=os.environ['ksbqirnakrdgji'],
                    password=os.environ['b2a4e8c890bd2da698980e5e14e4e73c43139f14c114d4fa8961866c1fe3cdc8'])
            # Open a cursor to perform database operations
                    cur = conn.cursor()

                    # Execute a command: this creates a new table
                    cur.execute('DROP TABLE IF EXISTS books;')
                    cur.execute('CREATE TABLE books (id serial PRIMARY KEY,'
                                                     'title varchar (150) NOT NULL,'
                                                     'author varchar (50) NOT NULL,'
                                                     'pages_num integer NOT NULL,'
                                                     'review text,'
                                                     'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                                     )

                    # Insert data into the table

                    cur.execute('INSERT INTO books (title, author, pages_num, review)'
                                'VALUES (%s, %s, %s, %s)',
                                ('A Tale of Two Cities',
                                 'Charles Dickens',
                                 489,
                                 'A great classic!')
                                )


                    cur.execute('INSERT INTO books (title, author, pages_num, review)'
                                'VALUES (%s, %s, %s, %s)',
                                ('Anna Karenina',
                                 'Leo Tolstoy',
                                 864,
                                 'Another great classic!')
                                )

                    conn.commit()

                    cur.close()
                    conn.close()
        else:
            pass # unknown
        
       

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
