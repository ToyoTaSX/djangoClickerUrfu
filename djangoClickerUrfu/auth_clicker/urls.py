from django.urls import include, path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('registration/', views.user_registration, name="registration"),
    path('users/<str:username>/', views.UsersDetailsList.as_view())
]
