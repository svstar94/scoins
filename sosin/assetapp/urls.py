from django.urls import path
from .views import *

app_name = 'assetapp'

urlpatterns = [
    path('create/', AssetCreateView.as_view(), name='create'),
    path('update/<int:pk>', AssetUpdateView.as_view(), name='update')
]
