from flask import Blueprint, request, jsonify
from models.addresses import Address
from schemas.addresses_schema import address_schema, addresses_schema
from main import db

address = Blueprint('address', __name__, url_prefix="/addresses")

# Gets the address data from a specified id number.
@address.get('/<int:id>')
def get_address(id):
    address = Address.query.get(id)
    return address_schema.dump(address)
    

# @address.get('/cc/<int:id>')
# def get_address(id):
#     address_fields = address_schema.load(request.json)
#     address = Address.query.filter_by(id=fields["id"]).first()
#     return jsonify("message")

# Gets an address of a specific childcare centre and returns the address
@address.get('/<int:childcare_centre_id>')
def get_childcare_address(childcare_centre_id):
    address = Address.query.filter_by(childcare_centre_id=childcare_centre_id).first()

    return address_schema.dump(address)


# Gets all the childcare centre ids according to suburb.
@address.get('/<string:suburb>')
def get_childcares_in_a_suburb(suburb):
    childcares = Address.query.filter_by(suburb=suburb).all()

    return addresses_schema.dump(childcares)

# Post an address for a childcare_centre (Childcare_centre must be listed first)
@address.post("/")
def create_address():
    try: 
        address_fields = address_schema.load(request.json)

        address = Address(**address_fields)
        db.session.add(address)
        db.session.commit()

    except:
        return { "message" : "Your information is incorrect"}

    return address_schema.dump(address)
