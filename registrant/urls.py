from django.urls import path

from registrant.views import (CreateUserView, DownloadQRCode,
                              HouseholdRegisterView, IndividualRegisterView,
                              RegistrantDashboard)

urlpatterns = [
    path('account/<str:registrant>/', CreateUserView, name="create-user"),
    path('register/household/', HouseholdRegisterView),
    path('register/individual/', IndividualRegisterView),
    path('<int:id>/', RegistrantDashboard),
    path('download/<int:id>/', DownloadQRCode),
]


