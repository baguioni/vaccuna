from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from core.views import RegistrantLoginView, LogoutRequest, LGULoginView, LandingPage

from vaccuna import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', LandingPage, name="vacuna"),
    path('login/', RegistrantLoginView, name="login-registrant"),
    path('logout/', LogoutRequest, name="logout"),
    path('admin/', admin.site.urls),
    path('registrant/', include('registrant.urls'), name='registrant'),
<<<<<<< HEAD
    path('lgu/', include('lgu.urls'), name='lgu')

=======
    path('lgu/', include('lgu.urls'), name='lgu'),
>>>>>>> 0a6d91ef22ee38558bfd2c112f98711f5ea801a0
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
