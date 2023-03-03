class Review(db.Model):

    __tablename__ = "reviews"

    id = db.Column(db.Integer(), primary_key=True)
    comment = db.Column(db.String())
    parent_rating = db.Column(db.Integer())
    date_posted = db.Column(db.Date())
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)