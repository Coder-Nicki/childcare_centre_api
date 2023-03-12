from main import db

class Address(db.Model):

    __tablename__ = "addresses"

    id = db.Column(db.Integer(), primary_key=True)
    street_number = db.Column(db.Integer())
    street_name = db.Column(db.String())
    suburb = db.Column(db.String())
    state = db.Column(db.String())
    postcode = db.Column(db.String())
    childcare_centre_id = db.Column(db.Integer(), db.ForeignKey("childcare_centres.id"), nullable=False)

    

    