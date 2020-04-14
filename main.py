from flask import Flask, render_template, url_for, request
from data import db_session
from data.car import Car


db_session.global_init("db/cars.sqlite")
session = db_session.create_session()

app = Flask(__name__)



@app.route("/")
def index():
    cars = session.query(Car)
    if request.args.get('name') != None:
        cars = cars.filter(Car.name.like(f"%"+request.args.get('name')+"%"))
    return render_template("index.html", cars=cars, title='Выбор тс')



def createCar(name='',
maxSpeed=0,mass=0,persons=4,engineType='',
buyPryce=0,sellPryce=0,mil14=0.0,mil12=0.0,
mil1=0.0,control=0.0,stop=0.0,addedInGameDlS='',
clas='',privod='f'):
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
    app.run(port=8080, host='127.0.0.1')
