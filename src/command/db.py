from flask import Blueprint
from main import db
from models.users import User
from models.childcare_centres import ChildcareCentre
from models.addresses import Address
from models.reviews import Review
from models.vacancies import Vacancy
from main import bcrypt


db_cmd = Blueprint("db", __name__)

@db_cmd.cli.command('reset')
def reset_db():
    db.drop_all()
    print('Tables are dropped!')
    db.create_all()
    print('Tables created')

@db_cmd.cli.command('create')
def create_db():
    db.create_all()
    print('Tables created')


@db_cmd.cli.command('seed')
def seed_db():
    
    #Create the users first
    user1 = User(
        email = "saskia@email.com",
        password = bcrypt.generate_password_hash("password123").decode("utf-8"),
        admin = True,
        username = "Saskia"
    )
    db.session.add(user1)

    user2 = User(
        email = "tully@email.com",
        password = bcrypt.generate_password_hash("password456").decode("utf-8"),
        admin = False,
        username = "Tully"
    )
    db.session.add(user2)

    user3 = User(
        email = "nala@email.com",
        password = bcrypt.generate_password_hash("password789").decode("utf-8"),
        admin = False,
        username = "Nala"
    )
    db.session.add(user3)

    db.session.commit()
    
    print('Users are seeded')

    childcare1 = ChildcareCentre(
        name = "Village Childcare",
        cost_per_day = 143,
        maximum_capacity = 140,
        phone_number = "012345678",
        email_address = "village@gmail.com",
        description = "Great large centre situated right next to the main primary school in town",
        user_id = 2
    )
    db.session.add(childcare1)

    childcare2 = ChildcareCentre(
        name = "Bumblebees",
        cost_per_day = 128,
        maximum_capacity = 100,
        phone_number = "012345678",
        email_address = "bumblebees@gmail.com",
        description = "Popular centre in close to the centre of town",
        user_id = 3
    )
    db.session.add(childcare2)


    childcare3 = ChildcareCentre(
        name = "Bright Beginnings",
        cost_per_day = 80,
        maximum_capacity = 46,
        phone_number = "012345678",
        email_address = "brightbeginnings@gmail.com",
        description = "Small family orientated centre",
        user_id = 2
    )
    db.session.add(childcare3)

    db.session.commit()
    
    print('Childcare centres are seeded')


    address1 = Address(
        street_number = 5,
        street_name = "Hill Street",
        suburb = "Wodonga",
        state = "Vic",
        postcode = "3690",
        childcare_centre_id = 1
    )
    db.session.add(childcare1)

    address2 = Address(
        street_number = 10,
        street_name = "Huon Road",
        suburb = "Wodonga",
        state = "Vic",
        postcode = "3690",
        childcare_centre_id = 2
    )
    db.session.add(address2)

    address3 = Address(
        street_number = 25,
        street_name = "Snow street",
        suburb = "Albury",
        state = "NSW",
        postcode = "2640",
        childcare_centre_id = 3
    )
    db.session.add(address3)
    db.session.commit()
    
    print('Addresses are seeded')


    review1 = Review(
        comment = "The best centre ever. My kids love it here",
        parent_rating = 10,
        childcare_centre_id = 1,
        user_id = 2
    )

    db.session.add(review1)


    review2 = Review(
        comment = "Not happy with this centre. Very dirty.",
        parent_rating = 2,
        childcare_centre_id = 2,
        user_id = 3
    )
    
    db.session.add(review2)

    review3 = Review(
        comment = "The most amazing educators here.",
        parent_rating = 10,
        childcare_centre_id = 1,
        user_id = 1
    )
    
    db.session.add(review3)

    db.session.commit()
    print("Reviews are seeded")


    vacancy1 = Vacancy(
        baby_vacancies = True,
        toddler_vacancies = False,
        preschool_vacancies = True,
        childcare_centre_id = 1
    )
    
    db.session.add(vacancy1)

    vacancy2 = Vacancy(
        baby_vacancies = False,
        toddler_vacancies = False,
        preschool_vacancies = False,
        childcare_centre_id = 2
    )
    
    db.session.add(vacancy1)

    vacancy3 = Vacancy(
        baby_vacancies = True,
        toddler_vacancies = True,
        preschool_vacancies = True,
        childcare_centre_id = 3
    )
    
    db.session.add(vacancy3)

    db.session.commit()
    print("Vacancies are seeded")


 
@db_cmd.cli.command('drop')
def drop_db():
    db.drop_all()
    print('Tables are dropped!')