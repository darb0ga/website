import sqlite3
import folium as folium
from flask import Flask, render_template, make_response, request, session
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
#from geopy import Nominatim
import requests as requests
from flask import Flask, render_template, make_response, request, session
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from data.subjects import Subject
from data.users import User
from data.lessons import Lesson
from data import db_session
from forms.user import RegisterForm, LoginForm, LessonForm
from PIL import Image
from io import BytesIO

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
        if user and user.check_password(form.password.data) and user.role == 'Ученик':
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        elif user and user.check_password(form.password.data) and user.role == 'Учитель':
            login_user(user, remember=form.remember_me.data)
            return redirect("/teacher")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    subjects = db_sess.query(Subject)
    return render_template("index2.html", subject=subjects)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/profile')
@login_required
def prof():
    return render_template("profile.html")


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


@app.route("/form_lesson")
@login_required
def form_lesson():
    form = LessonForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        lesson = Lesson(
            name=form.name.data,
            time=form.time.data,
            place=form.place.data,
            about=form.about.data
        )
        db_sess.add(lesson)
        db_sess.commit()
        return redirect('/teacher')
    return render_template("form_lesson.html", title='Регистрация', form=form)


@app.route("/teacher")
@login_required
def teacher():
    db_sess = db_session.create_session()
    lessons = db_sess.query(Lesson).filter(Lesson.teacher_id == current_user.id).all()
    return render_template("teacher1.html", lesson=lessons)


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


@app.route('/subjects')
def subject():
    return render_template('subjects.html')


@app.route('/maps')
def maps():
    api_server = "http://static-maps.yandex.ru/1.x/"

    lon = "37.530887"
    lat = "55.703118"
    delta = "0.002"

    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": "map"
    }
    response = requests.get(api_server, params=params)
    Image.open(BytesIO(
        response.content)).show()
    return redirect('/')
    map = folium.Map(location=[56.11677, 47.26278],
                     zoom_start=4
                     )
    folium.Marker(location=[56.14677, 47.22278],
                  tooltip='Чебоксары',
                  icon=folium.Icon(color='red')
                  ).add_to(map)
    return map._repr_html_()


@app.route('/teachers')
def teachers():
    db_sess = db_session.create_session()
    teach = db_sess.query(User).filter(User.role == 'Учитель').all()
    return render_template('teachers.html', rows=teach)


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


# в будущем это будет обработка входа на определенный предмет(человек открывает английский,
# у него появляется страница с выбором конкретного занятия)
# 123.html открывает список карточек с такими занятиями(в каждой карточке указан класс, время, about, учитель )
@app.route('/lesson/<int:les_id>')
@login_required
def info(les_id):
    db_sess = db_session.create_session()
    lessons = db_sess.query(Subject).filter(Lesson.subject_id == les_id).all()
    return render_template('123.html', lesson=lessons)


@app.route("/redacter/<int:id>", methods=['GET', 'POST'])
@login_required
def redacter(id):
    form = RegisterForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id)
        if user:
            form.phone.data = user.phone
            form.email.data = user.email
            form.about.data = user.about_me
            db_sess.commit()
            return redirect('/profile')
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id)
        if user:
            user.phone = form.phone.data
            user.email = form.email.data
            user.about_me = form.about.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('redacter.html',
                           title='Редактирование профиля',
                           form=form
                           )


if __name__ == '__main__':
    main()
    app.run(port=5080, host='127.0.0.1')

# if current_user.is_authenticated:
# subjects = db_sess.query(Subject).filter(Subject.user_id == current_user.id).all()

