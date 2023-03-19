from flask import Blueprint, request, abort, jsonify
from models.users import User
from schemas.users_schema import user_schema, users_schema
from datetime import timedelta
from main import bcrypt, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


user = Blueprint('user', __name__, url_prefix='/users')

# Create a function to check whether a logged in user is an admin user or not
def admin_only():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user.admin == False:
        return abort(401, description="Sorry you are not an admin user")

# Gets a list of all users and their details, excluding password

@user.get('/')
@jwt_required()
def get_users():
    
    admin_only()
   
    users = User.query.all()

    if not users:
        return { "message" : "No users listed"}
    
    return users_schema.dump(users)


# Queries the database for a specifed user according to user id and returns user details
@user.get('/<int:id>')
@jwt_required()
def get_user(id):
   
    admin_only()

    user = User.query.get(id)

    if not user:
        return { "message" : "No user"}

    return user_schema.dump(user)


# Queries the database for all admin users and returns details
@user.get('/admins')
@jwt_required()
def get_admin_users():
    # First checks to see if user is an admin user
    admin_only() 

    admin_users = User.query.filter(User.admin == True).all()

    if not admin_users:
        return { "message" : "No admins"}

    return users_schema.dump(admin_users)


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
    try:
        user = User(**user_fields)
        user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")
        
        db.session.add(user)
        db.session.commit()
    
    except:
        return { "message" : "Your information is incorrect"}
   
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

    # there is not a user with that email or if the password is not correct send an error
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Incorrect username and password")
    
   
    expiry = timedelta(days=1)
    
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)

    return jsonify({"username":user.username, "token": access_token })


# Deletes a user

@user.delete('/<int:id>')
@jwt_required()
def delete_user(id):

     # Only an admin can delete a listing
    admin_only()
        
    user = User.query.get(id)

    if not user:
        return { "message" : "No user listed"}, 400
    
    db.session.delete(user)
    db.session.commit()

    return {"message" : "User removed successfully"}


# Need to do a logout feature
# @user.route("/logout")
# def user_logout():
#     return {"message" : "You have been logged out"}
