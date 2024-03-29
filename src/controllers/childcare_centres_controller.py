from flask import Blueprint, request, jsonify, json, abort
from models.childcare_centres import ChildcareCentre
from models.addresses import Address
from models.users import User
from models.reviews import Review
from controllers.users_controller import admin_only
from schemas.childcare_centres_schema import childcare_centre_schema, childcare_centres_schema
from schemas.addresses_schema import address_schema, addresses_schema
from schemas.reviews_schema import review_schema, reviews_schema
from main import db
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
        return {"message" : "No childcares listed under that capacity"}, 404

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
        return { "message" : "Your information is incorrect"}, 400

    return childcare_centre_schema.dump(childcare_centre)


# Update a childcare listing by id and return updated childcare details

@childcare_centre.route("/<int:id>/", methods=["PUT"])
@jwt_required()
def update_childcare_centre(id):
    
    # # Find it in the db
    childcare_fields = childcare_centre_schema.load(request.json)
    
    childcare = ChildcareCentre.query.get(id)

    if not childcare:
        return abort(404, description="No childcare exists")

    try:
        childcare.name = childcare_fields["name"]
        childcare.cost_per_day = childcare_fields["cost_per_day"]
        childcare.maximum_capacity = childcare_fields["maximum_capacity"]
        childcare.phone_number = childcare_fields["phone_number"]
        childcare.email_address = childcare_fields["email_address"]
        childcare.description = childcare_fields["description"]
        childcare.user_id = childcare_fields["user_id"]
    
    except:
          return { "message" : "Your information is incorrect"}, 400

    db.session.commit()
    return childcare_centre_schema.jsonify(childcare)

   
# Deletes a childcare_centre post

@childcare_centre.delete('/<int:id>')
@jwt_required()
def delete_childcare_centre(id):
    # Only an admin can delete a listing
    admin_only()

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
    
# Use a join table to get a list of childcares in a certain suburb with at least one high parent rating.
@childcare_centre.get('/help/<string:suburb>')
def get_help(suburb):
    result = db.session.query(ChildcareCentre)\
    .join(Address)\
    .join(Review)\
    .filter(Address.suburb == suburb)\
    .filter(Review.parent_rating == 10)\
    .all()
    return childcare_centres_schema.dump(result)


