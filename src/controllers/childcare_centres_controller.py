from flask import Blueprint, request, jsonify, json, abort
from models.childcare_centres import ChildcareCentre
from models.addresses import Address
from models.users import User
from schemas.childcare_centres_schema import childcare_centre_schema, childcare_centres_schema, ChildcareCentreSchema
from main import db
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity

childcare_centre = Blueprint('childcare_centre', __name__, url_prefix="/childcare_centres")

# Gets a list of all childcare centres posted and their details
@childcare_centre.get('/')
def get_childcare_centres():
    childcare_centres = ChildcareCentre.query.all()
    result = childcare_centres_schema.dump(childcare_centres)
    return result


# Gets a specific childcare centre according to id and displays details
@childcare_centre.get('/<int:id>')
def get_childcare_centre(id):
    childcare_centre = ChildcareCentre.query.get(id)

    if not childcare_centre:
        return { "message" : "No childcare centre listed"}

    return childcare_centre_schema.dump(childcare_centre)


# Lists the childcare centres in order from cheapest to most expensive.
@childcare_centre.get('/fee_range')
def order_childcare_centre_by_cost():
    cost_range = ChildcareCentre.query.order_by(ChildcareCentre.cost_per_day).all()
    return childcare_centres_schema.dump(cost_range)
    


# Gets the cheapest childcare centre and returns childcare details.
@childcare_centre.get('/cheapest')
def get_cheapest_childcare_centre():
    cheapest = ChildcareCentre.query.order_by(ChildcareCentre.cost_per_day).first()
    
    return childcare_centre_schema.dump(cheapest)


# List the childcares that have a capacity under 50
@childcare_centre.get('/small_centres')
def get_small_centres():
    small_centres = ChildcareCentre.query.filter(ChildcareCentre.maximum_capacity <= 50).order_by(ChildcareCentre.maximum_capacity).all()
    
    return childcare_centres_schema.dump(small_centres)


# List the childcares that have a capacity under the user's specified limit.
@childcare_centre.get('/maximum_capacity/<int:maximum_capacity>')
def get_list_of_centres_under_capacity(maximum_capacity):
    list_of_centres_under_capacity = ChildcareCentre.query.filter(ChildcareCentre.maximum_capacity <= maximum_capacity).order_by(ChildcareCentre.maximum_capacity).all()
    
    if not list_of_centres_under_capacity:
        return {"message" : "No childcares listed under that capacity"}
    return childcare_centres_schema.dump(list_of_centres_under_capacity)

# Creates a childcare centre post and then returns post. Must be logged in to post
@childcare_centre.post("/")
@jwt_required()
def create_childcare_centre():
    childcare_centre_fields = childcare_centre_schema.load(request.json)

    name = ChildcareCentre.query.filter_by(name=childcare_centre_fields["name"]).first()

    if name:
        # return an abort message to inform the user that a childcare listing already exists for this childcare
        return abort(400, description="Childcare centre already exists")

    try: 
        childcare_centre = ChildcareCentre(**childcare_centre_fields)
        
        db.session.add(childcare_centre)
        db.session.commit()

    except:
        return { "message" : "Your information is incorrect"}

    return childcare_centre_schema.dump(childcare_centre)


# Update a childcare listing by id and return updated childcare details

@childcare_centre.route("/<int:id>/", methods=["PUT"])
@jwt_required()
def update_childcare_centre(id):
    user_id = get_jwt_identity()
    
    # Find it in the db
    user = User.query.get(user_id)
    
    if not user.admin:
        return abort(401, description="Unauthorised user")
    
    childcare = ChildcareCentre.query.get(id)

    name = request.json['name']
    description = request.json['description']
    phone_number = request.json['phone_number']
    email_address = request.json['email_address']
    user_id = request.json['user_id']
    cost_per_day = request.json['cost_per_day']
    maximum_capacity = request.json['maximum_capacity']

    childcare.name = name
    childcare.phone_number = phone_number
    childcare.email_address = email_address
    childcare.maximum_capacity = maximum_capacity
    childcare.cost_per_day = cost_per_day
    childcare.description = description
    childcare.user_id = user_id

    db.session.commit()
    return childcare_centre_schema.jsonify(childcare)
    
    
    # #get the user id invoking get_jwt_identity
    # user_id = get_jwt_identity()
    # #Find it in the db
    # user = User.query.get(user_id)
    # #Make sure it is in the database
    # if not user:
    #     return abort(401, description="Invalid user")
    
    # # Stop the request if the user is not an admin
    # if not user.admin:
    #     return abort(401, description="Unauthorised user")
    # # find the childcare centre
    # childcare_centre = ChildcareCentre.query.filter_by(id=id).first()
    # #return an error if the card doesn't exist
    # if not childcare_centre:
    #     return abort(400, description= "No childcare centre details listed")

    # childcare = ChildcareCentre(**childcare_centre_fields)
    # #update the car details with the given values
    # # childcare_centre.name = childcare_centre_fields["name"]
    # # childcare_centre.cost_per_day = childcare_centre_fields["cost_per_day"]
    # # childcare_centre.maximum_capacity = childcare_centre_fields["maximum_capacity"]
    # # childcare_centre.phone_number = childcare_centre_fields["phone_number"]
    # # childcare_centre.email_address = childcare_centre_fields["email_address"]
    # # childcare_centre.description = childcare_centre_fields["description"]
    # # not taken from the request, generated by the server
    # # card.date = date.today()
    # # add to the database and commit
    # db.session.add(childcare)
    # db.session.commit()
    # #return the card in the response
    # return jsonify(childcare_centre_schema.dump(childcare))


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
    
    
# # Use a join table to get a list of childcares in a certain suburb under a price range.
# @childcare_centre.get('/help')
# def get_help():
#     result = db.session.execute('select ChildcareCentre.name, ChildcareCentre.cost_per_day, Address.suburb from ChildcareCentre, Address join ChildcareCentre on childcare_centres_id = childcare_centre_id where ChildcareCentre.cost_per_day < 100')
#     return childcare_centres_schema.dump(result)


