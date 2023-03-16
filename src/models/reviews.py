from main import db
from datetime import datetime

class Review(db.Model):

    __tablename__ = "reviews"

    id = db.Column(db.Integer(), primary_key=True)
    comment = db.Column(db.String())
    parent_rating = db.Column(db.Integer())
    date_posted = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
    childcare_centre_id = db.Column(db.Integer(), db.ForeignKey("childcare_centres.id"), nullable=False)

    user = db.relationship("User", backref="review", cascade="all, delete")
    childcare_centre = db.relationship('ChildcareCentre', backref='review', cascade="all, delete")