from django.urls import include, path
from . import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('registration/', views.UserRegistrationView.as_view(), name="registration"),
    #path('users/<str:username>/', views.UsersDetailsList.as_view())
]
