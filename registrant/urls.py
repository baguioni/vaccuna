from django.urls import path
from registrant.views import (HouseholdRegisterView, IndividualRegisterView,
                              RegistrantDashboard, DownloadQRCode, CreateUserView)


urlpatterns = [
    path('account/<str:registrant>/', CreateUserView, name="create-user"),
    path('register/household/', HouseholdRegisterView),
    path('register/individual/', IndividualRegisterView),
    path('<int:id>/', RegistrantDashboard),
    path('download/<int:id>/', DownloadQRCode),
]


