from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    text = StringField('Комментарий')
    user = IntegerField('Пользователь')
    submit = SubmitField('Отправить')
