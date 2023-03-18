from main import ma


class VacancySchema(ma.Schema):
    
    class Meta:
        fields = ("id", "baby_vacancies", "toddler_vacancies", "preschool_vacancies", "childcare_centre_id", "childcare_centre")
        load_only = ["childcare_centre_id", "id"]

    childcare_centre = ma.Nested("ChildcareCentreSchema", only=["name", "phone_number"])



vacancy_schema = VacancySchema()
vacancies_schema = VacancySchema(many=True)