from django.contrib import admin
from django.urls import path
from vaccuna import settings
from core.views import LoginView, LogoutRequest, QRCodeRead, UpdateVaccinationStatus
from registrant.views import (HouseholdRegisterView, IndividualRegisterView,
                              RegistrantDashboard, DownloadQRCode)

from lgu.views import DashboardView
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', LoginView, name="login"),
    path('lgu-dashboard/<int:lgu_id>', DashboardView, name='dashboard'),
    path('logout', LogoutRequest, name="logout"),
    path('register-household', HouseholdRegisterView),
    path('register-individual/', IndividualRegisterView),
    path('admin/', admin.site.urls),
    path('registrant/<int:id>', RegistrantDashboard),
    path('api/qrcode/<int:pk>', QRCodeRead),
    path('vaccination/status/<int:pk>', UpdateVaccinationStatus),
    path('registrant/download/<int:id>', DownloadQRCode)
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
