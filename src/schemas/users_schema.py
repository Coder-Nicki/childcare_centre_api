from main import ma


class UserSchema(ma.Schema):
    
    class Meta:
        fields = ("id", "username", "password", "admin", "email")
        load_only = ["password"]


user_schema = UserSchema()
users_schema = UserSchema(many=True)