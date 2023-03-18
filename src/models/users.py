from main import db

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    admin = db.Column(db.Boolean(), default=False)
    email = db.Column(db.String())

    childcare_centre = db.relationship('ChildcareCentre', backref='user', lazy=True)
    review = db.relationship('Review', backref='user', cascade="all, delete-orphan", lazy=True)



