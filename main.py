from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, redirect, render_template, url_for
app = Flask(__name__)


@app.route('/training/<prof>')
def index(prof):
    return render_template('training.html',
                           prof=('инженер' in prof.lower()),
                           inj=str(url_for('static', filename='img/inj.png')),
                           doc=str(url_for('static', filename='img/doc.png')))


if __name__ == "__main__":
    app.run(port=8080, host='127.0.0.1')
