from main import db

class Vacancy(db.Model):

    __tablename__ = "vacancies"

    id = db.Column(db.Integer(), primary_key=True)
    baby_vacancies = db.Column(db.Boolean())
    toddler_vacancies = db.Column(db.Boolean())
    preschool_vacancies = db.Column(db.Boolean())
    childcare_centre_id = db.Column(db.Integer(), db.ForeignKey("childcare_centres.id"), nullable=False)