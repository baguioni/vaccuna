from django.contrib import admin
from django.urls import path

from core.views import LoginView, LogoutRequest
from registrant.views import (HouseholdRegisterView, IndividualRegisterView,
                              RegistrantHome)

urlpatterns = [
    path("", LoginView, name="login"),
    path("logout", LogoutRequest, name="logout"),
    path('register-household', HouseholdRegisterView),
    path('register-individual/', IndividualRegisterView),
    path('admin/', admin.site.urls),
]
