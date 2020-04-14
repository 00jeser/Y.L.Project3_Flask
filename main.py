from flask import Flask, render_template, url_for
from data import db_session
from data.car import Car


db_session.global_init("db/cars.sqlite")
session = db_session.create_session()

app = Flask(__name__)

                           
@app.route("/")
def index():
    cars = session.query(Car)#.filter(Car.is_private != True)
    return render_template("index.html", cars=cars)


def createCar():
    car = Car()
    car.name = "Italy GTO"
    car.to100 = "2"
    car.maxSpeed = "500"
    car.addedInGameDlS = "1"
    session.add(car)
    session.commit()


if __name__ == "__main__":
    app.run(port=8080, host='127.0.0.1')
