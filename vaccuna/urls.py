from django.contrib import admin
from django.urls import path

from registrant.views import RegistrantHome, IndividualRegisterView, HouseholdRegisterView
from core.views import LoginView, LogoutRequest

urlpatterns = [
    path("", LoginView, name="login"),
    path("logout", LogoutRequest, name="logout"),
    path('register-household', HouseholdRegisterView),
    path('register-individual/', IndividualRegisterView),
    path('admin/', admin.site.urls),

]
