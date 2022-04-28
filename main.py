from flask import Flask, render_template, make_response, request, session
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from data.subjects import Subject
from data.users import User
from data import db_session
from forms.user import RegisterForm, LoginForm


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/trial.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == 1)

    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        db_sess.commit()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        subjects = db_sess.query(Subject).filter(Subject.user_id == current_user.id).first()
    else:
        subjects = db_sess.query(Subject)
    return render_template("index.html", news=subjects)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if form.age.data <= 0:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Введите существующий возраст")
        if form.age.data <= 7:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Вы слишком малы для нашего сайта!")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            phone=form.phone.data,
            email=form.email.data,
            role=form.role.data,
            about_me=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/subjects')
def subjects():
    return render_template('subjects.html')


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1')
