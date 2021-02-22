from django.contrib import admin
from django.urls import path
from vaccuna import settings
from core.views import LoginView, LogoutRequest
from registrant.views import (HouseholdRegisterView, IndividualRegisterView,
                              RegistrantHome)
from lgu.views import DashboardView
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', LoginView, name="login"),
    path('dashboard/<int:lgu_id>', DashboardView, name='dashboard'),
    path('logout', LogoutRequest, name="logout"),
    path('register-household', HouseholdRegisterView),
    path('register-individual/', IndividualRegisterView),
    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
