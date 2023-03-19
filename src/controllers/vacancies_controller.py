from flask import Blueprint, request, jsonify, abort
from models.vacancies import Vacancy
from models.childcare_centres import ChildcareCentre
from schemas.vacancies_schema import vacancy_schema, vacancies_schema
from main import db
from flask_jwt_extended import jwt_required

vacancy = Blueprint('vacancy', __name__, url_prefix="/vacancies")
    

# Gets the vacancies of a specific childcare centre and returns the vacancy results 
@vacancy.get('/<int:childcare_centre_id>')
def get_childcare_vacancies(childcare_centre_id):
    
    childcare = ChildcareCentre.query.get(childcare_centre_id)
    
    if not childcare:
        return {"message": "This childcare centre does not exist in our system"}, 404

    vacancy = Vacancy.query.filter_by(childcare_centre_id=childcare_centre_id).first()

    if not vacancy:
        return abort(404, "No vacancies listed for this childcare centre")

    return vacancy_schema.dump(vacancy)


# List the childcares that have a vacancy in at least one age group.
@vacancy.get('/')
def get_list_of_centres_with_a_vacancy():
    get_list_of_centres_with_a_vacancy = Vacancy.query\
    .filter((Vacancy.baby_vacancies == "true") | (Vacancy.toddler_vacancies == "true") | (Vacancy.preschool_vacancies == "true"))\
    .all()
    
    if not get_list_of_centres_with_a_vacancy:
        return {"message" : "No childcares listed with any vacancies"}, 404

    return vacancies_schema.dump(get_list_of_centres_with_a_vacancy)



# Posts the vacancies for a childcare centre

@vacancy.post("/")
@jwt_required()
def create_vacancy():
    
    vacancy_fields = vacancy_schema.load(request.json)
    vacancy = Vacancy.query.filter_by(childcare_centre_id=vacancy_fields["childcare_centre_id"]).first()

    if vacancy:
        # return an abort message to inform the user that a childcare listing already exists for this childcare
        return abort(400, description="This childcare already has a vacancy listed")
    try:
        vacancy = Vacancy(**vacancy_fields)

    
        db.session.add(vacancy)
        db.session.commit()

    except:
        return { "message" : "Your information is incorrect"}, 400

    return vacancy_schema.dump(vacancy)


# Update a childcare's vacancy listing by childcare centre id and return updated vacancy details

@vacancy.put("/<int:childcare_centre_id>/")
@jwt_required()
def update_vacancies(childcare_centre_id):
    childcare = ChildcareCentre.query.get(childcare_centre_id)
    
    if not childcare:
        return {"message": "This childcare centre does not exist in our system"}, 400

    # # Find it in the db
    vacancy_fields = vacancy_schema.load(request.json)
    
    vacancy = Vacancy.query.get(childcare_centre_id)

    if not vacancy:
        return abort(404, description="No vacancy listed for this childcare centre")

    try:
        vacancy.baby_vacancies = vacancy_fields["baby_vacancies"]
        vacancy.toddler_vacancies = vacancy_fields["toddler_vacancies"]
        vacancy.preschool_vacancies = vacancy_fields["preschool_vacancies"]
        vacancy.childcare_centre_id = vacancy_fields["childcare_centre_id"]
    
    except:
          return { "message" : "Your information is incorrect"}, 400

    db.session.commit()
    return vacancy_schema.jsonify(vacancy)