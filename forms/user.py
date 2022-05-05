from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, EmailField, IntegerField, \
    RadioField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    role = RadioField('Введите вашу роль на сайте', choices=['Учитель', 'Ученик'])
    age = IntegerField('Возраст', validators=[DataRequired()])
    phone = IntegerField('Номер телефона(начиная со 2 числа, к примеру, 9172714253)', validators=[DataRequired()])
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class LessonForm(FlaskForm):
    name = StringField('Название урока', validators=[DataRequired()])
    time = StringField('Время проведения(в формате 00:00)', validators=[DataRequired()])
    place = StringField('Место проведения(для онлайн занятий: ссылка)', validators=[DataRequired()])
    about = TextAreaField("Описание урока")
    submit = SubmitField('Сохранить')
