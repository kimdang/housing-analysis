from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse 
from django.http import Http404
from execute import run_query

from django.template import loader

from myapp.models import indexTable

from myapp.forms import NewUser, FormName, InputCity

from .. import execute

def index(request):
    mydict = {"hi": "Lam", "hello": "Ngan"}
    return render(request, "myapp/index.html", mydict)

def test_db(request):
    city = indexTable.objects.order_by("regionID")
    return render(request, "myapp/test.html", {"city" : city})


def form_name_view(request):
    form = FormName()
    if request.method == "POST":
        form = FormName(request.POST)
        if form.is_valid():
            print("VALIDATION COMPLETED.")
            print("Name: " + form.cleaned_data['name'])

    return render(request, "myapp/form_name.html", {'form': form})


def users(request):
    form = NewUser()
    if request.method == "POST":
        form = NewUser(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print("FORM IS INVALID.")
    return render(request, 'myapp/users.html', {'form':form})

######## YOUR WORK STARTS HERE ######


class Housing ():
    def get(self, request, state, city):

        getIDquery = "SELECT * FROM myapp_indextable WHERE (regionName = '%s' and regionState = '%s')" %(city, state)
        regionID = execute.run_query(getIDquery, fetch=True, fetch_option='fetchone')['regionID']

# from .models import Question

# def index(request):
#     question_list = Question.objects.all()
#     template = loader.get_template('myapp/index.html')
#     context = {'question_list': question_list}
#     return HttpResponse(template.render(context, request))

#     """
#     if you do this, you don't have to import loader, see detail() below as example 
#     def index (request):
#         ... 
#         question_list = Question.objects.all()
#         context = {'question_list': question_list}
#         return render(request, 'myapp/index.html', context)
#     """

#     # Context is a dictionary mapping template variable names to Python objects.

#     # render(request object, template name, optional dictionary)
#     # render() returns HttpResponse object of given template rendered with given context

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'myapp/detail.html', {'question':question})

# """
# how to raise 404 error without using get_object_or_404()
# def detail (request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'myapp/detail.html', {'question': question})
# """

# def result(request, question_id):
#     return HttpResponse("You're looking at the result of question %s." %question_id)

# def comment(request, question_id):
#     # need content here
#     return HttpResponse("Ngan was here")


