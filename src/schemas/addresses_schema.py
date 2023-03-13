from main import ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.addresses import Address

class AddressSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Address
        include_relationships = True
        load_instance = True
        include_fk = True

# class AddressSchema(ma.Schema):
    
#     class Meta:
#         fields = ("id", "street_number", "street_name", "suburb", "state", "postcode", "childcare_centre_id", "childcare_centre")
#         # load_only = ["childcare_centre_id", "id"]

    childcare_centre = ma.Nested("ChildcareCentreSchema", exclude=["user"])



address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)