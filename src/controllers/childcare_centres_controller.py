from flask import Blueprint, request, jsonify, json
from models.childcare_centres import ChildcareCentre
from models.addresses import Address
from models.users import User
from schemas.childcare_centres_schema import childcare_centre_schema, childcare_centres_schema, ChildcareCentreSchema
from main import db
from datetime import date
from flask_jwt_extended import jwt_required

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
    try: 
        childcare_centre_fields = childcare_centre_schema.load(request.json)

        childcare_centre = ChildcareCentre(**childcare_centre_fields)
        
        db.session.add(childcare_centre)
        db.session.commit()

    except:
        return { "message" : "Your information is incorrect"}

    return childcare_centre_schema.dump(childcare_centre)


# Update a childcare listing by id and return updated childcare details

# @childcare_centre.put('/<int:id>')
# def update_childcare_centre(id):
#     childcare_centre = ChildcareCentre.query.filter_by(id=id).first()
#     # childcare_centre = ChildcareCentre.query.get(id = 'id')
#     childcare_centre_fields = childcare_centre_schema.load(request.json)

#     childcare_centre = ChildcareCentre(**childcare_centre_fields)
#     childcare_centre.phone_number = "123459876"
    
#     db.session.update()
#     db.session.commit()
    
#     result = childcare_centre_schema.dump(childcare_centre)

#     return result


    # # childcare_centre = ChildcareCentre.query.get(id)

    # childcare_centre_fields = childcare_centre_schema.load(request.json)
    # # find the user
    # # id = ChildcareCentre.query.filter_by(id=user_fields["id"]).first()
    # name = ChildcareCentre.query.filter_by(name=childcare_centre_fields["name"]).first()

    # if not name:
    #     return {"message": "No childcare centre listed"}

    # # childcare_centre_fields = childcare_centre_schema.load(request.json)

    # # childcare_centre = ChildcareCentre(**childcare_centre_fields)

    # # db.session.commit()

    # return childcare_centre_schema.dump(childcare_centre)

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


