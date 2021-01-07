
from .views import *
from django.urls import path

app_name = 'homeapp'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    # path('news/', NewsView.as_view(), name='news')
]
