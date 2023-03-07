from flask import Blueprint, request
from models.childcare_centres import ChildcareCentre
from schemas.childcare_centres_schema import childcare_centre_schema, childcare_centres_schema
from main import db

childcare_centre = Blueprint('childcare_centre', __name__, url_prefix="/childcare_centres")


@childcare_centre.get('/')
def get_childcare_centres():
    childcare_centres = ChildcareCentre.query.all()
    return childcare_centres_schema.dump(childcare_centres)


@childcare_centre.get('/<int:id>')
def get_childcare_centre(id):
    childcare_centre = ChildcareCentre.query.get(id)

    if not childcare_centre:
        return { "message" : "No childcare listed"}

    return childcare_centre_schema.dump(childcare_centre)


@childcare_centre.post("/")
def create_childcare_centre():
    # try: 
    childcare_centre_fields = childcare_centre_schema.load(request.json)

    childcare_centre = ChildcareCentre(**childcare_centre_fields)

   
    db.session.add(childcare_centre)
    db.session.commit()

    # except:
    #     return { "message" : "Your information is incorrect"}

    return childcare_centre_schema.dump(childcare_centre)