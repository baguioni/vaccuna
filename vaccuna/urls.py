from django.contrib import admin
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.urls import path

from core.views import LoginView, LogoutRequest
from lgu.views import (DashboardView, PriorityLocationCreate,
                       PriorityLocationDelete, PriorityLocationUpdate,
                       VaccinationSiteCreate, VaccinationSiteDelete,
                       VaccinationSiteUpdate)
from registrant.views import (HouseholdRegisterView, IndividualRegisterView,
                              RegistrantDashboard)
from vaccuna import settings
from lgu.views import DashboardView
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', LoginView, name="login"),
    path('lgu/<int:lgu_id>', DashboardView, name='dashboard'),
    path('logout', LogoutRequest, name="logout"),
    path('register/household', HouseholdRegisterView),
    path('register/individual', IndividualRegisterView),
    path('admin/', admin.site.urls),
    path('lgu/<int:lgu_id>/vaccination-site/create', VaccinationSiteCreate),
    path('lgu/<int:lgu_id>/vaccination-site/update/<int:vs_id>', VaccinationSiteUpdate),
    path('lgu/<int:lgu_id>/vaccination-site/delete/<int:vs_id>', VaccinationSiteDelete),
    path('lgu/<int:lgu_id>/priority-location/create', PriorityLocationCreate),
    path('lgu/<int:lgu_id>/priority-location/update/<int:pl_id>', PriorityLocationUpdate),
    path('lgu/<int:lgu_id>/priority-location/delete/<int:pl_id>', PriorityLocationDelete),
    path('registrant/<int:id>', RegistrantDashboard),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
