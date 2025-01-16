from django.urls import path
from . import views

urlpatterns = [
    path('api_working/', views.sample_api, name='sample-api'),
]