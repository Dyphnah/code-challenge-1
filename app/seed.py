
from models import Restaurant, Pizza, RestaurantPizza, db
from faker import Faker
import random
from app import app

fake = Faker()
db.init_app(app)
app.app_context().push()


def seed_data():
    with app.app_context():
        Restaurant.query.delete()
        RestaurantPizza.query.delete()
        Pizza.query.delete()
        db.session.commit()

        restaurants = []
        for _ in range(10):
            restaurant = Restaurant(
                name=f'The {fake.name()}',
                address=fake.address()
            )
            restaurants.append(restaurant)
            db.session.add(restaurant)

        db.session.commit()

        pizza_sizes = ['Large', 'Medium', 'Small']
        pizzas = []
        for _ in range(10):
            pizza = Pizza(
                name=f'{random.choice(pizza_sizes)} {fake.word()} Pizza',
                ingredients=fake.sentence()
            )
            pizzas.append(pizza)
            db.session.add(pizza)

        db.session.commit()

        price_list = [12, 23, 3, 17, 23, 12, 30, 19, 23, 10, 21]
        for _ in range(10):
            rest_piz = RestaurantPizza(
                pizza_id=random.choice(pizzas).id,
                restaurant_id=random.choice(restaurants).id,
                price=random.choice(price_list)
            )
            db.session.add(rest_piz)

        db.session.commit()


if __name__ == "__main__":
    seed_data()
