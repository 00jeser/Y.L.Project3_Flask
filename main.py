from flask import Flask, render_template, url_for, request, redirect
from data import db_session
from data.car import Car
from data.user import User
from data.comment import Comments
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.loginform import LoginForm
from data.commentsform import CommentForm
from data.registerform import RegisterForm
import json
import os
import random


db_session.global_init("db/cars.sqlite")
session = db_session.create_session()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/post', methods=['POST'])
def main():
    filter = request.json
    cars = session.query(Car)
    if "name" in filter.keys():
        cars = cars.filter(Car.name.like(f"%"+filter["name"]+"%"))
    if "minPrice" in filter.keys():
        cars = cars.filter(Car.buyPryce > int(filter["minPrice"]))
    if "maxPrice" in filter.keys():
        cars = cars.filter(Car.buyPryce < int(filter["maxPrice"]))
    if "timeTo1mile" in filter.keys():
        cars = cars.filter(Car.mil1 <= filter["timeTo1mile"])
    if "class" in filter.keys():
        cars = cars.filter(Car.clas == filter["class"])
    rezult = list()
    for car in cars:
        rez = dict()
        rez["name"] = car.name
        rez["maxSpeed"] = car.maxSpeed
        rez["mass"] = car.mass
        rez["persons"] = car.persons
        rez["engineType"] = car.engineType
        rez["buyPryce"] = car.buyPryce
        rez["sellPryce"] = car.sellPryce
        rez["timeTo1mile"] = car.mil1
        rez["class"] = car.clas
        rez["privod"] = car.privod
        rez["addedInGameDlS"] = car.addedInGameDlS
        rezult.append(rez)
    return json.dumps(rezult)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter(
            User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/backup')
def backup():
    return render_template("backup.html", path=url_for('db', filename='cars.sqlite'))


@app.route('/info/<car>', methods=['GET', 'POST'])
def info(car):
    form = CommentForm()
    if form.validate_on_submit():
        comm = Comments()
        comm.carId = car
        comm.content = form.text.data
        comm.user = form.user.data
        session.add(comm)
        session.commit()
        return redirect("/info/"+car)
    cars = session.query(Car)[int(car)-1]
    comms = session.query(Comments).filter(Comments.carId == cars.id)
    users = session.query(User)
    return render_template("info.html", path=str(cars.id), car=cars, comms=comms,users=users,form=form)


@app.route('/register', methods=['GET', 'POST'])
def reg():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = User()
        user.username = form.username.data
        user.admin = False
        user.user_id = len(list(session.query(User).filter(
            User.username == form.username.data)))
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        login_user(user)
        return redirect("/")
    return render_template('register.html', title='Авторизация', form=form)


@app.route("/test")
def test():
    return "it worked"


@app.route("/")
def index():
    cars = session.query(Car)
    if request.args.get('name') != None:
        cars = cars.filter(Car.name.like(f"%"+request.args.get('name')+"%"))
    return render_template("index.html", cars=cars, title='Выбор тс')


@app.route("/compare")
def compare():
    carsIds = list(map(int, request.args.get('cars').split('_')))
    cars = session.query(Car).filter(Car.id.in_(carsIds))
    return render_template("compare.html", cars=cars, path=url_for('static', filename='previev'), title='Выбор тс')


@app.route("/select", methods=['POST', 'GET'])
def select():
    cars = session.query(Car)
    if request.args.get('name') != None:
        cars = cars.filter(Car.name.like(f"%"+request.args.get('name')+"%"))

    if request.method == 'GET':
        return render_template("select.html", path='/'.join(url_for('static', filename='previev/1.jpg').split('/')[:-1]), cars=cars, title='Выбор тс')
    elif request.method == 'POST':
        return redirect(url_for('compare')+'?cars=' + '_'.join(request.form))


def createCar(name='',
              maxSpeed=0, mass=0, persons=4, engineType='',
              buyPryce=0, sellPryce=0, mil14=0.0, mil12=0.0,
              mil1=0.0, control=0.0, stop=0.0, addedInGameDlS='',
              clas='', privod='f'):
    car = Car()
    car.name = name
    car.maxSpeed = maxSpeed
    car.mass = mass
    car.persons = persons
    car.engineType = engineType
    car.buyPryce = buyPryce
    car.sellPryce = sellPryce
    car.mil1 = mil1
    car.mil12 = mil12
    car.mil14 = mil14
    car.control = control
    car.stop = stop
    car.addedInGameDlS = addedInGameDlS
    car.clas = clas
    car.privod = privod
    session.add(car)
    session.commit()


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')
