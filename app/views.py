from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

def Index(request):

    params={'name':'zaman','place':'Lahore'}
    return render(request, 'index.html',params)

def brand_register(request):
    return render(request,'brand_register.html')

def brand_login(request):
    return render(request,'brand_login.html')
