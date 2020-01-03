from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('class_path_web.core.urls', 'core'), namespace="core")),
    path(
        'accounts/',
        include(
            ('class_path_web.accounts.urls', 'accounts'),
            namespace="accounts"
        )
    ),
    path(
        'location/',
        include(
            ('class_path_web.location.urls', 'location'),
            namespace="location"
        )
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
