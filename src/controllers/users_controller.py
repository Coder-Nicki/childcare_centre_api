from flask import Blueprint, request, abort, jsonify
from models.users import User
from schemas.users_schema import user_schema, users_schema
from main import db
from datetime import timedelta
from main import bcrypt
from flask_jwt_extended import create_access_token

user = Blueprint('user', __name__, url_prefix='/users')

# Gets a list of all users and their details
@user.get('/')
def get_users():
    users = User.query.all()
    return users_schema.dump(users)

@user.get('/user_email')
def get_user_email():
    users = User.query.all()
    list = users_schema.dump(users)
    return jsonify(list[0]["email"])


# Queries the database for a specifed user according to user.id
@user.get('/<int:id>')
def get_user(id):
    user = User.query.get(id)

    if not user:
        return { "message" : "No user"}

    return user_schema.dump(user)


# Registers a new user and provides an access token
@user.route("/register", methods=["POST"])
def user_register():

    user_fields = user_schema.load(request.json)
    # find the user
    user = User.query.filter_by(email=user_fields["email"]).first()
    username = User.query.filter_by(username=user_fields["username"]).first()

    if user:
        # return an abort message to inform the user. That will end the request
        return abort(400, description="Email already registered")
    if username:
        return abort(400, description="Username already taken")

    # Create the user object
    user = User()
   
    user.username = user_fields["username"]
  
    user.email = user_fields["email"]
  
    user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")
   
    user.admin = user_fields["admin"]
   
    db.session.add(user)
    db.session.commit()
    #create a variable that sets an expiry date
    expiry = timedelta(days=1)
    #create the access token
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
  
    return jsonify({"username":user.username, "token": access_token })


# Logins an already existing user
@user.route("/login", methods=["POST"])
def user_login():

    user_fields = user_schema.load(request.json)
    #find the user in the database by email
    user = User.query.filter_by(email=user_fields["email"]).first()
    # there is not a user with that email or if the password is no correct send an error
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Incorrect username and password")
    
   
    expiry = timedelta(days=1)
    
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)

    return jsonify({"username":user.username, "token": access_token })


@user.route("/logout")
def user_logout():
    pass
