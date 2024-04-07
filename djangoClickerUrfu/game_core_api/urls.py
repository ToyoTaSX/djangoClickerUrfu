from django.urls import path
from . import views

boosts_list = views.BoostViewSet.as_view({
    'get': 'list',
})

boosts_buy = views.BoostViewSet.as_view({
    'put': 'update',
})

urlpatterns = [
    path('boosts/list/', boosts_list, name='boosts_list'),
    path('boosts/buy/<int:id>/', boosts_buy),
    path('click/', views.ClickView.as_view(), name='click'),
    path('get_core/', views.GetCoreView.as_view(), name='core')
]