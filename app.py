"""
Default Users: User(name='John', password='qwerty'), User(name='Paul', password='defcon'), User(name='Marie', password='sunshine')

john = User.query.filter_by(name='John').first()
john.post(
    'New properties of magnetism that could change our computers',
    'Our electronics can no longer shrink and are on the verge of overheating. But in a new discovery from the University of Copenhagen, researchers have uncovered a fundamental property of magnetism, which may become relevant for the development of a new generation of more powerful and less hot computers.',
    2022)

marie = User.query.filter_by(name='Marie').first()
marie.post(
    'Minecraft: Log4j 0day',
    'A new vulnerability has been found in the form of an exploit within Log4j, a Java logging library. This vulnerability poses a potential risk of your computer being compromised.',
    2021
)

paul = User.query.filter_by(name='Paul').first()
paul.post(
    'The one-click attack',
    'Cross-site request forgery (CSRF) is a type of malicious exploit of a website where unauthorized commands are submitted from a user that the web application trusts. In a CSRF attack auser is tricked by an attacker ( Using social engineering) to submit a malicious web request.',
    2022
"""

from flask import (Flask, render_template, redirect, request,
                   session, Response,  flash, render_template_string)

from forms import (LoginForm, RegisterForm)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import werkzeug


app = Flask(__name__)
app.secret_key = 'VulnCamp'

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vulnworld.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['WTF_CSRF_ENABLED'] = False
db = SQLAlchemy(app)


class Post(db.Model):
    """
    Blue print for a post
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    body = db.Column(db.String(100), default=None)
    created_at = db.Column(db.Integer, default=2020)
    author_id = db.Column(db.Integer, unique=True)


class User(db.Model):
    """
    Blue print for a user

    Methods:
    ========
    post: Creates a post and adds it to the database.s
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    bio = db.Column(db.String(80), default=None)
    created_at = db.Column(db.Integer, default=2020)

    def post(self, title: str, body: str, created_at: str) -> None:
        post = Post(title=title, body=body,
                    created_at=created_at, author_id=self.id)
        db.session.add(post)
        db.session.commit()


def create_user(users: list) -> list[User]:
    """
    Add users to the database

    Parameters:
    ===========
    users: list (default [])

    Raises:
    TypeError -- if <users> is not a list

    """
    for user in users:
        if not isinstance(user, User):
            raise TypeError('<users> must be a list of User objects')
        db.session.add(user)
    db.session.commit()
    return users


@app.before_request
def require_login() -> Response | None:
    """
    Redirects to the /register page if the user is not logged in.
    """
    allowed_routes = ['login', 'register']
    if 'username' not in session:
        if not request.path.startswith('/static'):
            if request.endpoint not in allowed_routes:
                return redirect('/register')
    if request.endpoint == 'admin' and session['username'] != 'Paul':
        return redirect('/')

        

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles the registration of new users.
    """
    form = RegisterForm()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(name=username).first()
        if existing_user:
            flash('That username already exists', 'error')
        else:
            new_user = create_user([User(name=username, password=password)])[
                0]  # Get the object
            db.session.add(new_user)
            db.session.commit()
            session['username'] = new_user.name
            flash('Logged in',  'info')

            return redirect('/')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles the login of existing users.
    """
    form = LoginForm()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(name=username).first()
        if existing_user and existing_user.password == password:
            session['username'] = existing_user.name
            flash('Logged in', 'info')
            return redirect('/')
        else:
            flash('Wrong username or password', 'error')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')


@app.route('/')
def index():
    """
    Displays the index page.
    """
    user = User.query.filter_by(name=session['username']).first()
    posts = []

    for index, post in enumerate(db.session.query(Post)):
        """
        Generates a tuple containing the post data as a dict and the author's name.
        """
        posts.append((post.__dict__, User.query.filter_by(
            id=post.author_id).first().name))

    return render_template('index.html', user=user, posts=posts, flag="v0lN{F0rg3_7h4t_C00k13}" if session['username'] == "Paul" else None)

@app.route('/admin')
def admin():
    with open('./secret/id_rsa',  'r')  as f:
        key = f.readlines()
    return render_template('admin.html', key=key)
    
if __name__ == '__main__':
    app.run()
