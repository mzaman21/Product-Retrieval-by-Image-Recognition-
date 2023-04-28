import json
from django.shortcuts import render,redirect
from .models import Brand,Product,PImage
from django.http import JsonResponse
from django.shortcuts import render
from .forms import BrandForm
from django.contrib import  messages
from django.core import serializers
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

            messages.error(request,"Brand Credentials")
            return render(request, 'brand_login.html')

    return render(request,'brand_login.html')

def brand_dashboard(request):

    BrandId = request.COOKIES['Brand_ID']
    brands = Brand.objects.filter(id=BrandId)

    for brand in brands:
        CBrand = Brand(Brand_Name=brand.Brand_Name, Brand_Email=brand.Brand_Email, Brand_Password=brand.Brand_Password,
                       Brand_Address=brand.Brand_Address, Brand_City=brand.Brand_City, Brand_State=brand.Brand_State,
                       Brand_Zip=brand.Brand_Zip, Brands_Logo=brand.Brands_Logo)


    Brand_Products = Product.objects.filter(Product_Brand__Brand_Name__contains=CBrand.Brand_Name)
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


def product_delete(request):
    print("in delete")
    if request.method=='POST':
       data=json.load(request)
       Pid=data.get('product_id')
       print(Pid)
       product_tobe_deleted = Product.objects.filter(id=Pid)
       print(product_tobe_deleted)
       product_tobe_deleted.delete()

       return JsonResponse({'status':'Product Deleted'})
    return JsonResponse({'status':"Product Not Deleted"})

def product_to_update(request):
    if request.method=='POST':
        data = json.load(request)
        Pid = data.get('product_id')
        print(Pid)
        # product_tobe_update = Product.objects.filter(id=Pid)
        # print(product_tobe_update)
        # for product in product_tobe_update:
        #  PUpdate = Product(Product_Name=product.Product_Name,Product_Price=product.Product_Price,Product_Category=product.Product_Category,Product_Description=product.Product_Description,Product_Stock=product.Product_Stock,Product_Brand=product.Product_Brand)
        # print(PUpdate)
        data = serializers.serialize("json",Product.objects.filter(id=Pid))
        print(data)
        return JsonResponse({'PUpdate':data,"Productid":Pid})
    return JsonResponse({'status':'Product to be update is not available'})

def product_update(request):
    if request.method=='POST':
        Pid = request.POST.get("Prid")
        Product_name = request.POST.get("Product_Name")
        Product_price = request.POST.get("Product_Price")
        Product_category = request.POST.get("Product_Category")
        Product_description = request.POST.get("Product_Description")
        Product_stock = request.POST.get("Product_Stock")
        print("in update")
        print(Pid)

        Product.objects.filter(id=Pid).update(Product_Name=Product_name,Product_Price=Product_price,Product_Category=Product_category,Product_Description=Product_description
                                              ,Product_Stock=Product_stock)
    return  redirect('brand_dashboard')
