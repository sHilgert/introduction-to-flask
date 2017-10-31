from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://intro_flask:intro_flask@localhost:5432/introduction_flask'
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_HASH'] = 'plaintext'

db = SQLAlchemy(app)

# Define models
roles_users = db.Table('roles_users',
  db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
  db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  description = db.Column(db.String(255))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), unique=True)
  password = db.Column(db.String(255))
  active = db.Column(db.Boolean())
  confirmed_at = db.Column(db.DateTime())
  roles = db.relationship('Role', secondary=roles_users,
                          backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.route('/')
def index():
  return "hi!"
  users = User.query.all()
  return render_template('index.html', users=users)

# @app.route('/user')
# def new_user():
#   return render_template('new_user.html')

@app.route('/profile/<email>')
@login_required
def profile(email):
  user = User.query.filter_by(email=email).first()
  return render_template('profile.html', user=user)


# @app.route('/user', methods=['POST'])
# def create_user():
#   user = User(request.form['username'], request.form['email'])
#   db.session.add(user)
#   db.session.commit()
#   return redirect(url_for('index'))

if __name__ == "__main__":
  app.run(debug = True)