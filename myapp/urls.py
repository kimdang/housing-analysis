from django.urls import path 
from . import views


app_name = 'myapp'


urlpatterns = [
    path('', views.identifyTarget, name='index'),
    path('showResult', views.showResult, name='result')
    # path('<int:question_id>/results/', views.result, name='result'),
    # the argument name is called by {% url %} template tag in index.html 
]



"""
The path() function pass 4 arguments: route, view, kwargs and name
route - string that contains URL pattern 

"""