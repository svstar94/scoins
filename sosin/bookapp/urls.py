

app_name = 'bookapp'

from django.urls import path

from .views import *

urlpatterns=[
    path('create/', BookCreateView.as_view(), name='create'),
    path('detail/', BookDetailView, name='detail'),
    path('delete/<int:pk>', BookDeleteView.as_view(), name='delete'),
]