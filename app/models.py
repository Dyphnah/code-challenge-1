from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    restaurant_pizzas = db.relationship(
        'RestaurantPizza', backref='restaurant')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }

    def __repr__(self):
        return f'Restaurant(id={self.id}, name={self.name}, address={self.address})'


class Pizza(db.Model):
    __tablename__ = 'pizzas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f'Pizza(id={self.id}, name={self.name}, ingredients={self.ingredients})'


class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('price')
    def check_price(self, key, price):
        if not (1 <= price <= 30):
            raise ValueError('Please enter a value between 1 and 30')
        return price

    def to_dict(self):
        return {
            'id': self.id,
            'pizza_id': self.pizza_id,
            'restaurant_id': self.restaurant_id,
            'price': self.price,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f'RestaurantPizza(price={self.price})'
