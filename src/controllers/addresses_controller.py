from flask import Blueprint, request
from models.addresses import Address
from schemas.addresses_schema import address_schema, addresses_schema
from main import db

address = Blueprint('address', __name__, url_prefix="/addresses")


@address.get('/<int:id>')
def get_address(id):
    address = Address.query.get(id)

    return address_schema.dump(address)


@address.post("/")
def create_address():
    # try: 
    address_fields = address_schema.load(request.json)

    address = Address(**address_fields)
    db.session.add(address)
    db.session.commit()

    # except:
    #     return { "message" : "Your information is incorrect"}

    return address_schema.dump(address)
