from django.urls import path 

from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.housing, name='test'),
    # path('<int:question_id>', views.detail, name='detail'),
    # path('<int:question_id>/results/', views.result, name='result'),
    # path('comment', views.comment, name='comment')
    # # the name value is called by {% url %} template tag in index.html 
]

"""
The path() function pass 4 arguments: route, view, kwargs and name
route - string that contains URL pattern 

"""