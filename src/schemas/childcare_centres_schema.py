from main import ma

class ChildcareCentreSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ("id", "name", "cost_per_day", "maximum_capacity", "user", "address", "phone_number", "email_address", "description", "user_id", "address_id")
        load_only = ["user_id", "address_id"]

    address = ma.Nested("AddressSchema")
    user = ma.Nested("UserSchema", exclude=["email", "id"])
    


childcare_centre_schema = ChildcareCentreSchema()
childcare_centres_schema = ChildcareCentreSchema(many=True)
