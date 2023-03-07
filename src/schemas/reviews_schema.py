from main import ma

class ReviewSchema(ma.Schema):
    class Meta:
        fields = ("id", "comment", "parent_rating", "date_posted", "user_id", "user", "childcare_centre_id", "childcare_centre")
        load_only = ["user_id", "childcare_centre_id"]

    user = ma.Nested("UserSchema")
    childcare_centre = ma.Nested("ChildcareCentreSchema")


review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)