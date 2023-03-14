from flask import Blueprint, request, jsonify, abort
from models.addresses import Address
from schemas.addresses_schema import address_schema, addresses_schema
from main import db
from flask_jwt_extended import jwt_required

address = Blueprint('address', __name__, url_prefix="/address")

# Gets the address data from a specified id
@address.get('/<int:id>')
def get_address(id):
    address = Address.query.get(id)

    if not address:
        return abort(404, "No address listed for this id")

    return address_schema.dump(address)

# Gets a list of all addresses
@address.get('/')
def get_addresses():
    address = Address.query.all()

    if not address:
        return abort(404, "No addresses listed")

    return addresses_schema.dump(address)
    

# Gets an address of a specific childcare centre and returns the address and childcare centre details
@address.get('/childcare_centre/<int:childcare_centre_id>')
def get_childcare_address(childcare_centre_id):
    address = Address.query.filter_by(childcare_centre_id=childcare_centre_id).first()

    if not address:
        return abort(404, "No address listed for this childcare centre")

    return address_schema.dump(address)


# Gets all the childcare centre ids according to suburb and returns childcare centre details and address
@address.get('/<string:suburb>')
def get_childcares_in_a_suburb(suburb):
    childcares = Address.query.filter_by(suburb=suburb).all()

    if not childcares:
        return abort(404, "No childcares listed for this suburb")

    return addresses_schema.dump(childcares)


# Gets all the childcare centre ids according to postcode and returns childcare centre details and address
@address.get('/postcode/<string:postcode>')
def get_childcares_in_a_postcode(postcode):
    childcares = Address.query.filter_by(postcode=postcode).all()

    if not childcares:
        return abort(404, "No childcares listed for this postcode")

    return addresses_schema.dump(childcares)


# Post an address for a childcare_centre (Childcare_centre must be listed first)
# then returns the address with specific childcare details

@address.post("/")
@jwt_required()
def create_address():
    
    address_fields = address_schema.load(request.json)
    address = Address.query.filter_by(childcare_centre_id=address_fields["childcare_centre_id"]).first()

    if address:
        # return an abort message to inform the user that a childcare listing already exists for this childcare
        return abort(400, description="Address already exists for this childcare centre")
    try:
        address = Address(**address_fields)

    
        db.session.add(address)
        db.session.commit()

    except:
        return { "message" : "Your information is incorrect"}, 400

    return address_schema.dump(address)

