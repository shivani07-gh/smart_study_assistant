from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_file, name='upload'),
    path('chat/', views.ask_question, name='chat'),
    path('history/', views.history, name='history'),
    path('delete/<int:doc_id>/', views.delete_file, name='delete_file'),
]