from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('notes/', views.notes_view, name='notes'),
    path('create/', views.create_note, name='create_note'),
]