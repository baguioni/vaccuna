from django.conf.urls import include
from django.contrib import admin
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.urls import path

from core.views import (LandingPage, LGULoginView, LogoutRequest,
                        RegistrantLoginView)
from vaccuna import settings

urlpatterns = [
    path('', LandingPage, name="home"),
    path('login/', RegistrantLoginView, name="login-registrant"),
    path('logout/', LogoutRequest, name="logout"),
    path('admin/', admin.site.urls),
    path('registrant/', include('registrant.urls'), name='registrant'),
    path('lgu/', include('lgu.urls'), name='lgu'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
