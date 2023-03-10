from flask import Blueprint, request, jsonify
from models.childcare_centres import ChildcareCentre
from schemas.childcare_centres_schema import childcare_centre_schema, childcare_centres_schema
from main import db
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity

childcare_centre = Blueprint('childcare_centre', __name__, url_prefix="/childcare_centres")

# Gets a list of all childcare centres posted
@childcare_centre.get('/')
def get_childcare_centres():
    childcare_centres = ChildcareCentre.query.all()
    return childcare_centres_schema.dump(childcare_centres)


# Gets a specific childcare centre according to id
@childcare_centre.get('/<int:id>')
def get_childcare_centre(id):
    childcare_centre = ChildcareCentre.query.get(id)

    if not childcare_centre:
        return { "message" : "No childcare listed"}

    return childcare_centre_schema.dump(childcare_centre)


# # Finds a childcare centre according to cost_per_day
# @childcare_centre.get("/cost")
# def get_childcare_address():
#     # childcare_centre_fields = childcare_centres_schema.load(request.json)
#     cost = ChildcareCentre.query.order_by(cost_per_day=cost_per_day).all()

#     return jsonify(cost)


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

    return jsonify(childcare_centre_schema.dump(childcare_centre))

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