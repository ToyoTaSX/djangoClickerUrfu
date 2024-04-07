from django.urls import include, path
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("auth_clicker.urls")),
    path('api/', include("game_core_api.urls")),
    path('', include("user_frontend.urls")),
]
