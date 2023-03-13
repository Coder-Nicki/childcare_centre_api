from main import ma


class ChildcareCentreSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "cost_per_day", "maximum_capacity", "user", "review", "phone_number", "email_address", "description", "user_id", "address_id", "address")
        load_only = ["user_id", "address_id"]


    user = ma.Nested("UserSchema", only=["username"])
    address = ma.Nested("AddressSchema", only=["suburb"])
    review = ma.Nested("ReviewSchema", only=["comment"])
    


childcare_centre_schema = ChildcareCentreSchema()
childcare_centres_schema = ChildcareCentreSchema(many=True)
