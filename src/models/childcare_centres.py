from main import db

class ChildcareCentre(db.Model):

    __tablename__ = "childcare_centres"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    cost_per_day = db.Column(db.Integer())
    maximum_capacity = db.Column(db.Integer())
    phone_number = db.Column(db.String())
    email_address = db.Column(db.String())
    description = db.Column(db.String())
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=True)

    address = db.relationship('Address', backref='childcare_centre', uselist=False, cascade="all, delete", lazy=True)
    review = db.relationship('Review', backref='childcare_centre', lazy=True, cascade="all, delete")
    vacancy = db.relationship('Vacancy', backref='childcare_centre', uselist=False, cascade="all, delete", lazy=True)

    