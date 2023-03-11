from flask import Blueprint, request
from models.reviews import Review
from schemas.reviews_schema import review_schema, reviews_schema
from main import db
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity

review = Blueprint('review', __name__, url_prefix="/reviews")


@review.get('/')
def get_reviews():
    reviews = Review.query.all()
    return reviews_schema.dump(reviews)


@review.get('/<int:id>')
def get_review(id):
    review = Review.query.get(id)

    if not review:
        return { "message" : "No reviews posted"}

    return review_schema.dump(review)


@review.post("/")
@jwt_required()
def create_review():
    try: 
        review_fields = review_schema.load(request.json)

        review = Review(**review_fields)

        db.session.add(review)
        db.session.commit()

    except:
        return { "message" : "Your information is incorrect"}

    return review_schema.dump(review)