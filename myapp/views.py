from django.shortcuts import render
from django.http import HttpResponse 

def index(request):
    return HttpResponse("WELCOME TO HOUSING MARKET ANALYSIS")
