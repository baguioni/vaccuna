from django.urls import path
from registrant.views import (HouseholdRegisterView, IndividualRegisterView,
                              RegistrantDashboard, DownloadQRCode)


urlpatterns = [
    path('register/household/', HouseholdRegisterView),
    path('register/individual/', IndividualRegisterView),
    path('<int:id>/', RegistrantDashboard),
    path('download/<int:id>/', DownloadQRCode),
]


