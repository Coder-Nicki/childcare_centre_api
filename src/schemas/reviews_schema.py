from main import ma

class ReviewSchema(ma.Schema):
    class Meta:
        fields = ("id", "comment", "parent_rating", "date_posted", "user", "user_id", "childcare_centre", "childcare_centre_id")
        load_only = ["user_id", "childcare_centre_id"]

    childcare_centre = ma.Nested("ChildcareCentreSchema", only=["name"])
    user = ma.Nested("UserSchema", only=["username"])


review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)