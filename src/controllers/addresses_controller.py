from flask import Blueprint, request, jsonify
from models.addresses import Address
from schemas.addresses_schema import address_schema, addresses_schema
from main import db
from flask_jwt_extended import jwt_required

address = Blueprint('address', __name__, url_prefix="/address")

# Gets the address data from a specified id
@address.get('/<int:id>')
def get_address(id):
    address = Address.query.get(id)
    return address_schema.dump(address)
    

# Gets an address of a specific childcare centre and returns the address and childcare centre details
@address.get('/childcare_centre/<int:childcare_centre_id>')
def get_childcare_address(childcare_centre_id):
    address = Address.query.filter_by(childcare_centre_id=childcare_centre_id).first()

    return address_schema.dump(address)


# Gets all the childcare centre ids according to suburb and returns childcare centre details and address
@address.get('/<string:suburb>')
def get_childcares_in_a_suburb(suburb):
    childcares = Address.query.filter_by(suburb=suburb).all()

    return addresses_schema.dump(childcares)


# Post an address for a childcare_centre (Childcare_centre must be listed first)
# then returns the address with specific childcare details

@address.post("/")
# @jwt_required()
def create_address():
    # try: 
    address = Address.query.filter_by(childcare_centre_id=childcare_centre_id).first()
    address_fields = address_schema.load(request.json)

    address = Address(**address_fields)

 
    db.session.add(address)
    db.session.commit()

    # except:
    #     return { "message" : "Your information is incorrect"}

    return address_schema.dump(address)

