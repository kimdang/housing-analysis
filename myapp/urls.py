from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.index, name='index')
]

"""
The path() function pass 4 arguments: route, view, kwargs and name
route - string that contains URL pattern 

"""