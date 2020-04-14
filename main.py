from flask import Flask, render_template, url_for, request, redirect
from data import db_session
from data.car import Car


db_session.global_init("db/cars.sqlite")
session = db_session.create_session()

app = Flask(__name__)

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
