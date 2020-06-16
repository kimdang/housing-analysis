from django.shortcuts import render
from django.http import HttpResponse 

from .models import Question

def index(request):
    question_list = Question.objects.all()
    output = ', '.join([q.question_text for q in question_list])
    return HttpResponse(output)

def detail (request, question_id):
    return HttpResponse("You're looking at %s question" % question_id)

def result(request, question_id):
    return HttpResponse("You're looking at the result of %s question." %question_id) 


