from flask import Blueprint, request
from models.reviews import Review
from models.users import User
from models.childcare_centres import ChildcareCentre
from controllers.users_controller import admin_only
from schemas.reviews_schema import review_schema, reviews_schema
from main import db
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity

review = Blueprint('review', __name__, url_prefix="/reviews")


@review.get('/')
def get_reviews():
    reviews = Review.query.all()
    return reviews_schema.dump(reviews)

# Get review by childcare id and return childcare details and review
@review.get('/<int:id>')
def get_review(id):
    review = Review.query.get(id)

    if not review:
        return { "message" : "No reviews posted"}

    return review_schema.dump(review)

# Get a list of reviews for a given childcare centre
@review.get('/childcare_reviews/<int:childcare_centre_id>')
def get_childcare_reviews(childcare_centre_id):

    childcare = ChildcareCentre.query.get(childcare_centre_id)
    
    if not childcare:
        return {"message": "This childcare centre does not exist in our system"}, 404

    childcare_reviews = Review.query.filter_by(childcare_centre_id=childcare_centre_id).all()

    if not childcare_reviews:
        return { "message" : "No reviews posted for this childcare centre"}, 404

    return reviews_schema.dump(childcare_reviews)


# Get a list of reviews for high parent ratings over 8.
@review.get('/rating')
def get_highest_parent_rating():
    rating = Review.query.filter(Review.parent_rating >= 8).all()

    if not rating:
        return { "message" : "No childcares listed have a high parent rating"}, 404

    return reviews_schema.dump(childcare_reviews)


@review.post("/")
@jwt_required()
def create_review():
    try: 
        review_fields = review_schema.load(request.json)

        review = Review(**review_fields)
        # Ensures that rating is between 0 and 10
        if review.parent_rating > 10 or review.parent_rating < 0:
            return {"message" : "Parent rating must be between 0 and 10"}
        db.session.add(review)
        db.session.commit()

    except:
        return { "message" : "Your information is incorrect"}

    return review_schema.dump(review)


# Deletes a childcare_centre post

@review.delete('/<int:id>')
@jwt_required()
def delete_review(id):
    # Only an admin can delete a listing
    admin_only()

    review = Review.query.get(id)

    if not review:
        return { "message" : "No review listed"}, 404
    
    db.session.delete(review)
    db.session.commit()

    return {"message" : "Review removed successfully"}, 200