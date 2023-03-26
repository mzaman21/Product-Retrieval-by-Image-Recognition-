from django.shortcuts import render,redirect
from .models import Brand
from django.http import HttpResponse
from django.shortcuts import render
from .forms import BrandForm
from django.contrib.auth import login, authenticate
from django.contrib import  messages
def Index(request):

    params={'name':'zaman','place':'Lahore'}
    return render(request, 'index.html',params)

def brand_register(request):
    if request.method == 'POST':
        context = {}
        # create object of form
        form = BrandForm(request.POST or  None, request.FILES or None)

        # check if form data is valid
        if form.is_valid():
            form.save()
        context['form'] = form
        return redirect('brand_login')
    return render(request,'brand_register.html')

def brand_login(request):
    if request.method=='POST':
        brand_email = request.POST['brand_email']
        brand_password = request.POST['brand_password']
        brand = Brand.objects.filter(Brand_Email=brand_email,Brand_Password=brand_password).values()
        print(brand)
        if brand.exists():
            print("in if")
            return redirect('brand_dashboard')
        else:
            print("fail")
            messages.error(request,"Brand Credentials")
            return render(request, 'brand_login.html')
    print("all fail")
    return render(request,'brand_login.html')

def brand_dashboard(request):
    return render (request,"brand_dashboard.html")

def prduct_add(request):

    return render(request,"product_add.html")