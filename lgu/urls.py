from django.urls import path

from core.views import LGULoginView
from lgu.views import (DashboardView, PriorityLocationCreate,
                       PriorityLocationDelete, PriorityLocationUpdate,
                       VaccinationSiteCreate, VaccinationSiteDelete,
                       VaccinationSiteUpdate, VaccinationSiteView)

urlpatterns = [
    path('login/', LGULoginView, name="login-lgu"),
    path('<int:lgu_id>/', DashboardView, name='dashboard'),
    path('<int:lgu_id>/vaccination-site/create/', VaccinationSiteCreate),
    path('<int:lgu_id>/vaccination-site/update/<int:vs_id>/', VaccinationSiteUpdate),
    path('<int:lgu_id>/vaccination-site/delete/<int:vs_id>/', VaccinationSiteDelete),
    path('<int:lgu_id>/priority-location/create/', PriorityLocationCreate),
    path('<int:lgu_id>/priority-location/update/<int:pl_id>/', PriorityLocationUpdate),
    path('<int:lgu_id>/priority-location/delete/<int:pl_id>/', PriorityLocationDelete),
    path('<int:lgu_id>/vaccination-site/<int:vs_id>/', VaccinationSiteView),
]


