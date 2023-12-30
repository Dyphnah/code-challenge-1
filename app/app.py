#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza
# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return "This is a trial"


@app.route('/restaurants')
def restaurant():

    restaurants = [restaurant.to_dict()
                   for restaurant in Restaurant.query.all()]

    response = make_response(
        jsonify(restaurants),
        200
    )
    return response


@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def single_restaurant(id):

    if request.method == 'GET':
        restaurant = Restaurant.query.filter_by(id=id).first()

        if restaurant == None:
            response = make_response(
                jsonify({
                    "error": "Restaurant not found"
                }),
                404
            )
            return response
        elif restaurant:

            response = make_response(
                jsonify(restaurant.to_dict()),
                200
            )
            return response
    elif request.method == 'DELETE':
        restaurant = Restaurant.query.filter_by(id=id).first()

        if restaurant:
            restaurant_pizza = RestaurantPizza.query.filter_by(
                restaurant_id=id).all()

            for item in restaurant_pizza:
                db.session.delete(item)
                db.session.commit()

            db.session.delete(restaurant)
            db.session.commit()

            response = make_response(
                jsonify({
                    "Delete_successful": True,
                    "message": "Restaurant successfully deleted."
                }),
                200
            )
            return response

        elif restaurant == None:
            response = make_response(
                jsonify({
                    "error": "Restaurant not found"
                }),
                404
            )
            return response


@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizza_list = []

    for pizza in pizzas:
        pizza_data = {
            'id': pizza.id,
            'name': pizza.name,
            'ingredients': pizza.ingredients
        }
        pizza_list.append(pizza_data)

    return jsonify(pizza_list)


@app.route('/restaurant_pizzas', methods=['GET', 'POST'])
def restaurant_pizzas():

    data = request.get_json()

    new_post = {
        "pizza_id": data["pizza_id"],
        "restaurant_id": data["restaurant_id"],
        "price": data["price"],
    }

    db.session.add(new_post)
    db.session.commit()

    response = make_response(
        jsonify(new_post.to_dict()),
        201
    )
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)

