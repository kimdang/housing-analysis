from django.urls import path 

from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.identifyTarget, name='index'),
    path('showResult', views.showResult, name='result')
    # path('test', views.test_db, name='test'),
    # path('form', views.form_name_view, name="form_name"),
    # path('signup', views.users, name="signup")
    # path('<int:question_id>/results/', views.result, name='result'),
    # path('comment', views.comment, name='comment')
    # # the name value is called by {% url %} template tag in index.html 
]

"""
The path() function pass 4 arguments: route, view, kwargs and name
route - string that contains URL pattern 

"""