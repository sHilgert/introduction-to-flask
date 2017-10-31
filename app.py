from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://intro_flask:intro_flask@localhost:5432/introduction_flask'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(80), unique = True)
  email = db.Column(db.String(120), unique = True)

  def __init__(self, username, email):
    self.username = username
    self.email = email

  def __repr__(self):
    return '<User %r>' % self.username

@app.route('/')
def index():
  users = User.query.all()
  return render_template('index.html', users=users)

@app.route('/user')
def new_user():
  return render_template('new_user.html')

@app.route('/profile/<username>')
def profile(username):
  user = User.query.filter_by(username=username).first()
  return render_template('profile.html', user=user)


@app.route('/user', methods=['POST'])
def create_user():
  user = User(request.form['username'], request.form['email'])
  db.session.add(user)
  db.session.commit()
  return redirect(url_for('index'))

if __name__ == "__main__":
  app.run(debug = True)