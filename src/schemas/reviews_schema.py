from main import ma

class ReviewSchema(ma.Schema):
    class Meta:
        fields = ("id", "comment", "parent_rating", "date_posted", "user_id", "childcare_centre_id")
    #     load_only = ["user_id", "childcare_centre_id"]

    # user = ma.Nested("UserSchema")


review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)