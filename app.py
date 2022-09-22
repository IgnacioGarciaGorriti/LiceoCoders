from flask import Flask, url_for, redirect, render_template, g, make_response, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from flask_wtf import CSRFProtect

from blueprints.books import books
from blueprints.users import users
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm
from models.user import User
from repository.user_repository import UserRepository

csrf = CSRFProtect()

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'c97c616e6d3821ba209cfc123a598d47d73a35bfcc84b52957c9316e1c2a01bc'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
csrf.init_app(app)

app.register_blueprint(users)
app.register_blueprint(books)

login_manager = LoginManager(app)
login_manager.login_view = 'login_template'


@login_manager.user_loader
def load_user(id):
    user_repository = UserRepository()
    user = user_repository.get(id)
    if user is not None:
        g.user = user
    return user


@app.get('/login')
def login_template():
    if current_user.is_authenticated:
        return redirect(url_for('hello_world'))
    form = LoginForm()

    return render_template('auth/login.html', form=form)


@app.get('/register')
def register_form():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    form = RegisterForm()
    return render_template('auth/register.html', form=form)


@app.post('/register')
def register():
    try:
        form = RegisterForm()
        if form.validate_on_submit():
            username = form.username.data
            name = form.name.data
            surname = form.surname.data
            email = form.email.data
            password = form.password.data
            age = form.age.data
            gender = form.age.data
            role = 'user'
            points = 0
            status = 'Beginner'

            user = User(username, name, surname, email, password, age, gender, role, points, status)
            user_repository = UserRepository()
            user_repository.add(user)
            login_user(user, remember=True)

            return redirect(url_for('hello'))

        return render_template('auth/register.html', form=form)
    except Exception as e:
        return make_response(e.__str__(), 400)


@app.post('/login')
def login():
    try:
        form = LoginForm()
        if form.validate_on_submit():
            user_repository = UserRepository()
            user = user_repository.get_by_email(form.email.data)
            if user is not None and user.check_password(form.password.data):
                login_user(user, remember=True)
                return redirect(url_for('hello'))

        return render_template('auth/login.html', form=form)
    except Exception as e:
        return make_response(e.__str__(), 400)


@app.get('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_template'))


@app.get('/')
def hello():
    flash('You were successfully logged in')
    return render_template('home/hello.html')


if __name__ == '__main__':
    app.run()
