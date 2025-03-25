from django.urls import path
from . import views

app_name = 'galaxia_app'

urlpatterns = [
    path('upload/', views.upload_documento, name='upload_documento'),
]
