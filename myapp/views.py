from django.shortcuts import render
from django.http import HttpResponse 

from django.template import loader

from .models import Question

def index(request):
    question_list = Question.objects.all()
    template = loader.get_template('myapp/index.html')
    context = {'question_list': question_list}
    return HttpResponse(template.render(context, request))

    """
    if you do this, you don't have to import loader
    def index (request):
        ... 
        question_list = Question.objects.all()
        context = {'question_list': question_list}
        return render(request, 'myapp/index.html', context)
    """

    # Context is a dictionary mapping template variable names to Python objects.

    # render(request object, template name, optional dictionary)
    # render() returns HttpResponse object of given template rendered with given context

def detail (request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist :(")
    return render(request, 'myapp/detail.html', {'question': question})

def result(request, question_id):
    return HttpResponse("You're looking at the result of %s question." %question_id) 


