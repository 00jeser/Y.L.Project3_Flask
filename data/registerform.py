from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    username = StringField('Имя')
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')