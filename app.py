from flask import Flask, render_template, session, redirect, request, url_for
from functools import wraps
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = b'P\xc4\xda~\x02\xb8\xdf\x11\x06RK1:\x96xg'

# Connection
client = MongoClient('localhost', 27017, username='admin', password='1234')
# Database
db = client.gn
# Collections
profesores = db.profesores

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')

  return wrap

# Routes
from user import routes

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
    all_colecciones = db.list_collection_names()
    all_profesores = profesores.find()
    return render_template('dashboard.html', colecciones=all_colecciones,profesores=all_profesores)
