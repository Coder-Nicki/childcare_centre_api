from flask import Blueprint, request, jsonify, json, abort
from models.childcare_centres import ChildcareCentre
from models.addresses import Address
from models.users import User
from models.reviews import Review
from schemas.childcare_centres_schema import childcare_centre_schema, childcare_centres_schema
from schemas.addresses_schema import address_schema, addresses_schema
from schemas.reviews_schema import review_schema, reviews_schema
from main import db
# from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity

childcare_centre = Blueprint('childcare_centre', __name__, url_prefix="/childcare_centres")

# Gets a list of all childcare centres posted and their details
@childcare_centre.get('/')
def get_childcare_centres():
    childcare_centres = ChildcareCentre.query.all()

    if not childcare_centres:
        return { "message" : "No childcare centres listed"}, 404

    result = childcare_centres_schema.dump(childcare_centres)
    return result


# Gets a specific childcare centre according to id and displays details
@childcare_centre.get('/<int:id>')
def get_childcare_centre(id):
    childcare_centre = ChildcareCentre.query.get(id)

    if not childcare_centre:
        return { "message" : "No childcare centre listed"}, 404

    return childcare_centre_schema.dump(childcare_centre)


# Lists the childcare centres in order from cheapest to most expensive.
@childcare_centre.get('/fee_range')
def order_childcare_centre_by_cost():
    cost_range = ChildcareCentre.query.order_by(ChildcareCentre.cost_per_day).all()

    if not cost_range:
        return {"message" : "No childcares listed with fees"}, 404

    return childcare_centres_schema.dump(cost_range)
    


# Gets the cheapest childcare centre and returns childcare details.
@childcare_centre.get('/cheapest')
def get_cheapest_childcare_centre():
    cheapest = ChildcareCentre.query\
    .order_by(ChildcareCentre.cost_per_day)\
    .first()
    
    if not cheapest:
        return {"message" : "No childcare centres are listed yet"}, 404

    return childcare_centre_schema.dump(cheapest)


# List the childcares that have a capacity under 50
@childcare_centre.get('/small_centres')
def get_small_centres():
    small_centres = ChildcareCentre.query\
    .filter(ChildcareCentre.maximum_capacity <= 50)\
    .order_by(ChildcareCentre.maximum_capacity)\
    .all()
    
    if not small_centres:
        return {"message" : "No childcare centres listed with a capacity under 50"}, 404

    return childcare_centres_schema.dump(small_centres)


# List the childcares that have a capacity under the user's specified limit.
@childcare_centre.get('/maximum_capacity/<int:maximum_capacity>')
def get_list_of_centres_under_capacity(maximum_capacity):
    list_of_centres_under_capacity = ChildcareCentre.query\
    .filter(ChildcareCentre.maximum_capacity <= maximum_capacity)\
    .order_by(ChildcareCentre.maximum_capacity)\
    .all()
    
    if not list_of_centres_under_capacity:
        return {"message" : "No childcares listed under that capacity"}

    return childcare_centres_schema.dump(list_of_centres_under_capacity)

# Creates a childcare centre post and then returns post. Must be logged in to post
@childcare_centre.post("/")
# @jwt_required()
def create_childcare_centre():
    childcare_centre_fields = childcare_centre_schema.load(request.json)

    name = ChildcareCentre.query.filter_by(name=childcare_centre_fields["name"]).first()

    if name:
        # return an abort message to inform the user that a childcare listing already exists for this childcare
        return abort(400, description="Childcare centre already exists")

    # try: 
    childcare_centre = ChildcareCentre(**childcare_centre_fields)
        
    db.session.add(childcare_centre)
    db.session.commit()

    # except:
    #     return { "message" : "Your information is incorrect"}, 400

    return childcare_centre_schema.dump(childcare_centre)


# Update a childcare listing by id and return updated childcare details

@childcare_centre.route("/<int:id>/", methods=["PUT"])
# @jwt_required()
def update_childcare_centre(id):
    # user_id = get_jwt_identity()
    
    # # Find it in the db
    # user = User.query.get(user_id)
    
    # if not user.id
    #     return abort(401, description="Unauthorised user")
    
    childcare = ChildcareCentre.query.get(id)

    if not childcare:
        return {"message" : "No childcare listed"}, 404

    try:

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

    except:
        return {"message" : "Your information is incorrect"}, 400
    



# Deletes a childcare_centre post

@childcare_centre.delete('/<int:id>')
# @jwt_required()
def delete_childcare_centre(id):
    # Only an admin can delete a listing
    # user_id = get_jwt_identity()
    
    # user = User.query.filter_by(id=user_id).first()
    
    # if user.admin == False:
    #     return abort(401, description="Sorry you are not an admin user")
    childcare_centre = ChildcareCentre.query.get(id)

    if not childcare_centre:
        return { "message" : "No childcare listed"}, 404
    
    db.session.delete(childcare_centre)
    db.session.commit()

    return {"message" : "Childcare centre removed successfully"}, 200
    

# Get childcare centre listings according to suburb and display childcare info and address
@childcare_centre.get("/address/<string:suburb>")
def get_childcares_by_suburb(suburb):
    result = db.session.query(ChildcareCentre)\
    .join(Address)\
    .filter(Address.suburb == suburb)\
    .all()

    if not result:
        return abort(404, "No childcares listed for this suburb")

    return childcare_centres_schema.dump(result)
    
# Use a join table to get a list of childcares in a certain suburb with a high parent rating.
@childcare_centre.get('/help/<string:suburb>')
def get_help(suburb):
    result = db.session.query(ChildcareCentre)\
    .join(Address)\
    .join(Review)\
    .filter(Address.suburb == suburb)\
    .filter(Review.parent_rating >= 8)\
    .all()
    return childcare_centres_schema.dump(result)


