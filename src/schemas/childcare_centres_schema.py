from main import ma
from marshmallow import fields

class ChildcareCentreSchema(ma.Schema):
    class Meta:
        fields = ("name", "cost_per_day", "maximum_capacity", "phone_number", "email_address", "description", "user_id", "user")
        load_only = ["user_id"]

        user = ma.Nested("UserSchema")


childcare_centre_schema = ChildcareCentreSchema()
childcare_centres_schema = ChildcareCentreSchema(many=True)
