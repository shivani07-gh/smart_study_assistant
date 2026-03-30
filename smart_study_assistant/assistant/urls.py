from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
]

from .views import upload_file

urlpatterns = [
    path('', upload_file),
]