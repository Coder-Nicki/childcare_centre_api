from flask import Blueprint, request, jsonify, json
from models.childcare_centres import ChildcareCentre
from models.addresses import Address
from models.users import User
from schemas.childcare_centres_schema import childcare_centre_schema, childcare_centres_schema
from main import db
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity

childcare_centre = Blueprint('childcare_centre', __name__, url_prefix="/childcare_centres")

# Gets a list of all childcare centres posted
@childcare_centre.get('/')
def get_childcare_centres():
    childcare_centres = ChildcareCentre.query.all()
    result = childcare_centres_schema.dump(childcare_centres)
    return result

@childcare_centre.get('/n')
def get_childcare_centresn():
    # childcare_addresses = ChildcareCentre.query.join(User).add_columns(ChildcareCentre.id, ChildcareCentre.name, User.id).filter(ChildcareCentre.id == User.id).all()
    cc = db.session.query(ChildcareCentre).join(User).all()
    return childcare_centres_schema.dump(cc)

# Gets a specific childcare centre according to id
@childcare_centre.get('/<int:id>')
def get_childcare_centre(id):
    childcare_centre = ChildcareCentre.query.get(id)

    if not childcare_centre:
        return { "message" : "No childcare listed"}

    return childcare_centre_schema.dump(childcare_centre)


# Lists the childcare centres in order from cheapest to most expensive.
@childcare_centre.get('/cost_range')
def order_childcare_centre_by_cost():
    cost_range = ChildcareCentre.query.order_by(ChildcareCentre.cost_per_day).all()
    return childcare_centres_schema.dump(cost_range)
    


# Gets the ccheapest childcare centres and returns childcare details.
@childcare_centre.get('/cheapest')
def get_cheapest_childcare_centre():
    cheapest = ChildcareCentre.query.order_by(ChildcareCentre.cost_per_day).first()
    
    return childcare_centre_schema.dump(cheapest)


# List the childcares that have a capacity under 50
@childcare_centre.get('/small_centres')
def get_small_centres():
    small_centres = ChildcareCentre.query.filter(ChildcareCentre.maximum_capacity <= 50).order_by(ChildcareCentre.maximum_capacity).all()
    
    return childcare_centres_schema.dump(small_centres)


# List the childcares that have a capacity under the searcher's specified limit.
@childcare_centre.get('/maximum_capacity/<int:maximum_capacity>')
def get_list_of_centres_under_capacity(maximum_capacity):
    list_of_centres_under_capacity = ChildcareCentre.query.filter(ChildcareCentre.maximum_capacity <= maximum_capacity).order_by(ChildcareCentre.maximum_capacity).all()
    
    return childcare_centres_schema.dump(list_of_centres_under_capacity)

# Creates a childcare centre post
@childcare_centre.post("/")
@jwt_required()
def create_childcare_centre():
    # try: 
    childcare_centre_fields = childcare_centre_schema.load(request.json)

    childcare_centre = ChildcareCentre(**childcare_centre_fields)
    
    db.session.add(childcare_centre)
    db.session.commit()

    # except:
    #     return { "message" : "Your information is incorrect"}

    return childcare_centre_schema.dump(childcare_centre)


# Update a childcare listing

@childcare_centre.put('/<int:id>')
def update_childcare_centre(id):
    childcare_centre = ChildcareCentre.query.get(id)
    if not childcare_centre:
        return {"message": "No childcare centre listed"}

    childcare_centre_fields = childcare_centre_schema.load(request.json)

    childcare_centre.name = childcare_centre_fields["name"]
    childcare_centre.cost_per_day = childcare_centre_fields["cost_per_day"]
    childcare_centre.maximum_capacity = childcare_centre_fields["maximum_capacity"]
    childcare_centre.phone_number = childcare_centre_fields["phone_number"]
    childcare_centre.email_address = childcare_centre_fields["email_address"]
    childcare_centre.description = childcare_centre_fields["description"]

    db.session.commit()

    return childcare_centre_schema.dump(childcare_centre)

# Deletes a childcare_centre post

@childcare_centre.delete('/<int:id>')
@jwt_required()
def delete_childcare_centre(id):
    childcare_centre = ChildcareCentre.query.get(id)

    if not childcare_centre:
        return { "message" : "No childcare listed"}
    
    db.session.delete(childcare_centre)
    db.session.commit()

    return {"message" : "Childcare centre removed successfully"}
    
    
# @childcare_centre.get('/location')
# def get_location():
#     location = ChildcareCentre.query.join(Address).all()
    
#     # return jsonify(location)
#     return childcare_centre_schema.dump(location)


