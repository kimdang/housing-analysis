from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>', views.detail, name='details'),
    path('<int:question_id>/results/', views.result, name='results')
]

"""
The path() function pass 4 arguments: route, view, kwargs and name
route - string that contains URL pattern 

"""