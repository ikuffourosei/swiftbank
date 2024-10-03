from django.urls import path
from sbank import views
urlpatterns = [
    path('', views.index, name='index')
]