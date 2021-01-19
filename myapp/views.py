from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from django.template import loader


# import form
from myapp.forms import InputCity



# other Python modules 
import execute
import tools
import SQLtools
import translateState
import computecity
import pandas as pd
import base64



# log user input 
from utils.user_data import ClientInfo # get user's IP address, etc.
import logging
logger = logging.getLogger('mylogger')



def identifyTarget(request):
    # index page receives city and state information from user
    form = InputCity()
    return render(request, 'myapp/index.html', {'form': form})



def showResult(request):


    form = InputCity()
    city = request.GET['city']
    state = request.GET['state']
    # additional form to receive city and state information from user


    requestData = ClientInfo(request).getData() # get user's IP address, etc.
    requestData['city'] = city
    requestData['state'] = state
    logger.info(requestData)


    # state names are abbreviated in MySQL database
    # enable to handle state names that are lowercase state, abbreviated, etc.
    if len(state) == 2:
        state = state.upper()
    else:
        try:
            state = translateState.state_dictionary.get(tools.capitalize_words(state), state)
        except TypeError:
            raise Http404('Invalid state. Please check your spelling!')

    
    # capitalize city name where appropriate 
    city = tools.capitalize_words(city)


    try:
        getIDquery = "SELECT * FROM main_index WHERE (cityname = '%s' and statename = '%s')" %(city, state)
        regionid = execute.run_query(getIDquery, fetch=True, fetch_option='fetchone')['regionid']
        # get regionid from main_index table
    except TypeError:
        raise Http404("Invalid location. Please check that your information is correct.")


    if regionid: 
        citydata = SQLtools.getDataFromDB(regionid, state)    
    else:
        raise Http404("This location is not in database.")
    


    # GRAPH historical data - midtier
    image_png = computecity.plothistory(citydata['midtier'])
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')


    # OBTAIN average value of each tier 
    citysummary = {}
    for tier in citydata:
        temp = citydata[tier]
        try:
            endprice = '$' + '{:,}'.format(temp['price'].iloc[-1]) # 'price' column, last row, add dollar sign
            citysummary.update({tier : endprice})
        except:
            endprice = 'N/A'
            citysummary.update({tier : endprice})


    # CALCULATE rise percentage
    percentperyear, latestdate = computecity.calcpercent(citydata['midtier'])


    # # Convert into appropriat form for purpose of display
    # targetDF['date'] = targetDF['date'].apply(lambda x: x.strftime('%B %d, %Y'))
    # targetDF['price'] = targetDF['price'].apply(lambda x: '${:,}'.format(x))

    info = {'city' : tools.capitalize_words(city), 
            'state' : state.upper(), 
            'graphic' : graphic, 
            'form' : form, 
            'citysummary': citysummary,
            'percentperyear' : percentperyear,
            'latestdate' : latestdate,
            }


    return render(request, 'myapp/displayresult.html', info)




"""
------------------ ARCHIVE ----------------------

# from .models import Question

# def index(request):
#     question_list = Question.objects.all()
#     template = loader.get_template('myapp/index.html')
#     context = {'question_list': question_list}
#     return HttpResponse(template.render(context, request))


#     if you do this, you don't have to import loader, see detail() below as example
#     def index (request):
#         ...
#         question_list = Question.objects.all()
#         context = {'question_list': question_list}
#         return render(request, 'myapp/index.html', context)


#     # Context is a dictionary mapping template variable names to Python objects.

#     # render(request object, template name, optional dictionary)
#     # render() returns HttpResponse object of given template rendered with given context

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'myapp/detail.html', {'question':question})

# how to raise 404 error without using get_object_or_404()
# def detail (request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'myapp/detail.html', {'question': question})


# def result(request, question_id):
#     return HttpResponse("You're looking at the result of question %s." %question_id)


# def index(request):
#     mydict = {"hi": "Lam", "hello": "Ngan"}
#     return render(request, "myapp/index.html", mydict)

# def test_db(request):
#     city = indexTable.objects.order_by("regionID")
#     return render(request, "myapp/test.html", {"city" : city})


# def form_name_view(request):
#     form = FormName()
#     if request.method == "POST":
#         form = FormName(request.POST)
#         if form.is_valid():
#             print("VALIDATION COMPLETED.")
#             print("Name: " + form.cleaned_data['name'])

#     return render(request, "myapp/form_name.html", {'form': form})


# def users(request):
#     form = NewUser()
#     if request.method == "POST":
#         form = NewUser(request.POST)
#         if form.is_valid():
#             form.save(commit=True)
#             return index(request)
#         else:
#             print("FORM IS INVALID.")
#     return render(request, 'myapp/users.html', {'form':form})

"""
