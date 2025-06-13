from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# herokuログ確認
from ecapp import views

handler500 = views.my_customized_server_error


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("ecapp.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
