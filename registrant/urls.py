from django.urls import path
from registrant.views import (HouseholdRegisterView, IndividualRegisterView,
                              RegistrantDashboard)


urlpatterns = [
    path('register/household/', HouseholdRegisterView),
    path('register/individual/', IndividualRegisterView),
    path('<int:id>/', RegistrantDashboard),
]


