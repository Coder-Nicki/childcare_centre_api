from main import ma


class AddressSchema(ma.Schema):
    
    class Meta:
        fields = ("id", "street_number", "street_name", "suburb", "state", "postcode", "childcare_centre_id")
        # load_only = ["childcare_centre_id"]

    # childcare_centre = ma.Nested("ChildcareCentreSchema")



address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)