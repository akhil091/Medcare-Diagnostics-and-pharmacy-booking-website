from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('All_Users.urls')),
    path('',include('Doctors.urls')),
    path('',include('Lab.urls')),
    path('',include('contact.urls')),
    path('',include('Medicine.urls')),
    # path('api-auth/',include('rest_framework.urls')),
    # path('api/token/',obtain_auth_token,name='obtain-token'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

