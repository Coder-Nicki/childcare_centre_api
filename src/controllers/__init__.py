from controllers.home_controller import home
from controllers.users_controller import user
from controllers.childcare_centres_controller import childcare_centre
from controllers.reviews_controller import review
from controllers.addresses_controller import address
from controllers.vacancies_controller import vacancy


registerable_controllers = [
    home,
    user,
    childcare_centre,
    review,
    address,
    vacancy,
]