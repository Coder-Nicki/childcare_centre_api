from flask import Blueprint
from main import db
from models.users import User

db_cmd = Blueprint("db", __name__)

@db_cmd.cli.command('create')
def create_db():
    db.create_all()
    print('Tables created')


@db_cmd.cli.command('seed')
def seed_db():
    
    #Create the users first
    user1 = User(
        email = "admin@email.com",
        password = "123456",
        admin = True,
        username = "Saskia"
    )
    db.session.add(user1)

    user2 = User(
        email = "tully@email.com",
        password = "123456",
        admin = False,
        username = "Nala"
    )
    db.session.add(user2)
    db.session.commit()
    
    print('Users are seeded')


@db_cmd.cli.command('drop')
def drop_db():
    db.drop_all()
    print('Tables are dropped!')