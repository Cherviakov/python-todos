from flask import Flask, request, redirect, url_for
from mako.lookup import TemplateLookup
from sqlalchemy.sql import insert, update, delete
import simplejson as json

import db

app = Flask(__name__)

@app.route('/')
def root():
  lookup = TemplateLookup(directories=['templates'], strict_undefined=True)
  template = lookup.get_template('main.html')
  s = db.session()
  todos = s.query(db.Todo).all()
  parsedTodos = []
  for todo in todos:
    parsedTodos.append(todo.toDict())
  return template.render(todo=parsedTodos)

@app.route('/todo', methods=['HEAD', 'GET', 'POST', 'PUT', 'DELETE'])
def todo():
  if request.method == 'HEAD':
    s = db.session()
    return json.dumps(s.query(db.Todo).count())
  elif request.method == 'GET':
    return redirect(url_for('root'))
  elif request.method == 'POST':
    s = db.session()
    s.execute(insert(db.Todo, request.form));
    s.commit()
    return redirect(url_for('root'))
  elif request.method == 'PUT':
    s = db.session()
    s.execute(update(db.Todo).where(db.Todo.id == int(request.args.getlist('id')[0])).values(label = str(request.data, 'utf-8')))
    s.commit()
    return 'todo updated';
  elif request.method == 'DELETE':
    s = db.session()
    s.query(db.Todo).filter(db.Todo.id == int(request.data)).delete()
    s.commit()
    return 'todo deleted' 
