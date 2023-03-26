from django.shortcuts import render,redirect
from .models import Brand,Product,PImage
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
        brands = Brand.objects.filter(Brand_Email=brand_email,Brand_Password=brand_password)

        if brands.exists():
           for brand in brands:
               BrandId = brand.id
           response = redirect('brand_dashboard')
           response.set_cookie('Brand_ID',BrandId)
           return response
        else:
            print("fail")
            messages.error(request,"Brand Credentials")
            return render(request, 'brand_login.html')
    print("all fail")
    return render(request,'brand_login.html')

def brand_dashboard(request):

    BrandId = request.COOKIES['Brand_ID']
    brands = Brand.objects.filter(id=BrandId)
    print(brands)
    for brand in brands:
        CBrand = Brand(Brand_Name=brand.Brand_Name, Brand_Email=brand.Brand_Email, Brand_Password=brand.Brand_Password,
                       Brand_Address=brand.Brand_Address, Brand_City=brand.Brand_City, Brand_State=brand.Brand_State,
                       Brand_Zip=brand.Brand_Zip, Brands_Logo=brand.Brands_Logo)

    print(CBrand.Brand_State)
    Brand_Products = Product.objects.filter(Product_Brand__Brand_Name__contains=CBrand.Brand_Name)
    print(CBrand)
    print(Brand_Products)
    context = {
        'BProducts': Brand_Products
    }
    return render (request,"brand_dashboard.html",context)

def product_add(request):
    if request.method=='POST':
        Product_name = request.POST.get("Product_Name")
        Product_price = request.POST.get("Product_Price")
        Product_category = request.POST.get("Product_Category")
        Product_description = request.POST.get("Product_Description")
        Product_stock = request.POST.get("Product_Stock")
        Product_images = request.FILES.getlist("Product_Image")
        BrandId = request.COOKIES['Brand_ID']
        brands = Brand.objects.filter(id=BrandId)
        for brand in brands:
            New_Product = Product(Product_Name=Product_name,Product_Price=Product_price,Product_Category=Product_category,Product_Description=Product_description,Product_Stock=Product_stock,Product_Brand=brand)
        New_Product.save()
        for image in Product_images:
            PImage(Product=New_Product,Product_Image=image).save()
        return redirect('brand_dashboard')

    return render(request,"product_add.html")