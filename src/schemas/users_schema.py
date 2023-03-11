from main import ma


class UserSchema(ma.Schema):
    
    class Meta:
        fields = ("id", "username", "password", "admin", "email")
        load_only = ["admin", "password"]

    # childcare_centre = ma.List(ma.Nested("ChildcareCentreSchema", exclude=["user"]))


user_schema = UserSchema()
users_schema = UserSchema(many=True)