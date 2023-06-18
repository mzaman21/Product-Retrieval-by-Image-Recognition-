import json
from django.shortcuts import render,redirect

from PRIR.settings import CART_SESSION_ID
from .cart import Cart,SProduct,OrderdProduct
from .models import Brand,Product,PImage,Customer,Order,OrderItem
from django.http import JsonResponse
from django.shortcuts import render
from .forms import BrandForm
from django.contrib import  messages
from django.core import serializers
from math import ceil
from django.template.defaulttags import register

import os
import cv2
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from skimage.metrics import structural_similarity as ssim
import numpy as np

from PIL import Image
def Index(request):

    products = Product.objects.all()                #retrive all products

    n=len(products)
    nslides = n//4 + ceil((n/4)-(n//4))

    productImages ={}
    for product in products:
        ProductImage = PImage.objects.filter(Product=product).values().first()
        productImages[product.id] = ProductImage

    params={'no_of_slides':nslides, 'range':range(1, nslides), 'product':products,"PImage":productImages}

    return render(request, 'index.html',params)

@register.filter
def get_item(dictionary, key):

    return dictionary[key]['Product_Image']

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

    allorders = Order.objects.all()
    ordercount=0
    productscount=0
    for orderItem in allorders:
        if orderItem.OrderDetail.BrandOrder.id == int(BrandId):
           ordercount=ordercount+1

    Brand_Products = Product.objects.filter(Product_Brand__Brand_Name__contains=CBrand.Brand_Name)

    for bproduct in Brand_Products:
        productscount=productscount+1

    context = {
        'BProducts': Brand_Products,
        'BrandName': CBrand.Brand_Name,
        'BrandLogo': CBrand.Brands_Logo,
        'OrdeCount': ordercount,
        'ProductCount':productscount
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

    if request.method=='POST':
       data=json.load(request)
       Pid=data.get('product_id')

       product_tobe_deleted = Product.objects.filter(id=Pid)

       product_tobe_deleted.delete()

       return JsonResponse({'status':'Product Deleted'})
    return JsonResponse({'status':"Product Not Deleted"})

def product_to_update(request):
    if request.method=='POST':
        data = json.load(request)
        Pid = data.get('product_id')

        data = serializers.serialize("json",Product.objects.filter(id=Pid))

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


        Product.objects.filter(id=Pid).update(Product_Name=Product_name,Product_Price=Product_price,Product_Category=Product_category,Product_Description=Product_description
                                              ,Product_Stock=Product_stock)
    return  redirect('brand_dashboard')


def get_single_product(request,slug):
    product = Product.objects.get(slug=slug)
    FImage = PImage.objects.filter(Product=product).first
    productsImages = PImage.objects.filter(Product=product)

    context = {'product': product, 'FeaturedImage': FImage, 'images': productsImages}

    return render(request, 'single_product.html', context=context)

def add_to_cart(request):
    if request.method=='POST':

        cart = Cart(request)
        pid = request.POST.get('productid')
        pquantity = request.POST.get('quantity')
        product = Product.objects.filter(id=pid)
        for p in product:
            Pslug = p.slug
            Prid = p.id

        cart.add(product_id=Prid, quantity=pquantity, update_quantity=False)
        messages.success(request, "The product was added to the cart.")

        return redirect("cart_detials")

    return render(request,"index.html")

def cart_detials(request):

    cart = Cart(request)

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)

    if change_quantity:
        cart.add(change_quantity, quantity, True)

    #get product present in current cart session
    product_in_cart_session = request.session[CART_SESSION_ID]

    cart_products=[]
    productImages={}

    one_product_total = 0
    cart_total = 0

    #get product and make product object and set relevent attributes and get thumbnail image also calculate total cart price
    for pid in product_in_cart_session:
        product = Product.objects.filter(id=pid)
        p_quantity_cart=product_in_cart_session[pid]['quantity']
        for p in product:
            make_product = SProduct(Product_id=p.id,Product_Name=p.Product_Name,Product_Price=p.Product_Price,
                            Product_Category=p.Product_Category,Product_Description=p.Product_Description,Product_Stock=p.Product_Stock,slug=p.slug,Quantity=p_quantity_cart)

            ProductImage = PImage.objects.filter(Product=p).values().first()
            productImages[p.id] = ProductImage
            cart_products.append(make_product)

            #convert price in string to int
            PPrice = int(make_product.Product_Price)

            one_product_total = make_product.Quantity*PPrice
            cart_total = cart_total+one_product_total

    context ={
        "cart_products":cart_products,
        "PImage":productImages,
        "total_cost":cart_total
    }
    return render(request,"cart_details.html",context)

def checkout(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']

        new_customer = Customer(name=name,email=email,phone=phone,address=address,city=city,state=state,zipcode=zip)
        new_customer.save()

        # get product present in current cart session
        product_in_cart_session = request.session[CART_SESSION_ID]

        for pid in product_in_cart_session:
            product = Product.objects.filter(id=pid)
            p_quantity_cart = product_in_cart_session[pid]['quantity']
            for p in product :
                create_order_item = OrderItem(CustomerOrder=new_customer,ProductOrder=p,BrandOrder=p.Product_Brand,
                                              ItemPrice=p.Product_Price,ItemQuantity=p_quantity_cart)
                create_order_item.save()

            new_order = Order(OrderDetail=create_order_item)
            new_order.save()


    return render(request,"checkout.html")

def brand_orders(request):

    BrandId = request.COOKIES['Brand_ID']
    brands = Brand.objects.filter(id=BrandId)

    for brand in brands:
        CBrand = Brand(Brand_Name=brand.Brand_Name, Brand_Email=brand.Brand_Email, Brand_Password=brand.Brand_Password,
                       Brand_Address=brand.Brand_Address, Brand_City=brand.Brand_City, Brand_State=brand.Brand_State,
                       Brand_Zip=brand.Brand_Zip, Brands_Logo=brand.Brands_Logo)

    allorders = Order.objects.all()

    brand_orderd_products=[]

    for orderItem in allorders:
        if orderItem.OrderDetail.BrandOrder.id == int(BrandId):

            product_total = orderItem.OrderDetail.ItemQuantity * int(orderItem.OrderDetail.ProductOrder.Product_Price)
            orderedProduct=OrderdProduct(Product_id=orderItem.OrderDetail.ProductOrder.id,
                                         Product_Name=orderItem.OrderDetail.ProductOrder.Product_Name,
                                         Product_Price=orderItem.OrderDetail.ProductOrder.Product_Price,
                                         Product_Category=orderItem.OrderDetail.ProductOrder.Product_Category,
                                         Product_Description=orderItem.OrderDetail.ProductOrder.Product_Description,
                                         Product_Stock=orderItem.OrderDetail.ProductOrder.Product_Stock,
                                         slug=orderItem.OrderDetail.ProductOrder.slug,
                                         Quantity=orderItem.OrderDetail.ItemQuantity,
                                         Total= product_total,
                                         CName= orderItem.OrderDetail.CustomerOrder.name,
                                         CEmail= orderItem.OrderDetail.CustomerOrder.email,
                                         CPhone= orderItem.OrderDetail.CustomerOrder.phone,
                                         CAddress= orderItem.OrderDetail.CustomerOrder.address,
                                         CCity= orderItem.OrderDetail.CustomerOrder.city,
                                         CState= orderItem.OrderDetail.CustomerOrder.state,
                                         CZipcode= orderItem.OrderDetail.CustomerOrder.zipcode,
                                         )

            brand_orderd_products.append(orderedProduct)


    context={
        "orders":brand_orderd_products
    }
    return render(request, "brand_orders.html",context)

def image_recognition(request):
    if request.method=='POST':

        # Get uploaded image
        dress = request.FILES['dress']
        print(dress)
        # Save the uploaded image to disk
        fs = FileSystemStorage()
        filename = fs.save(dress.name, dress)
        uploaded_file_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Read uploaded image and perform image processing
        img = cv2.imread(uploaded_file_path)
        # Resize the uploaded image to a fixed height of 300 pixels while maintaining the aspect ratio
        height = 300
        width = int(img.shape[1] * height / img.shape[0])
        img = cv2.resize(img, (width, height))
        # Convert image from BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Get list of images in a folder
        folder_path = os.path.join(settings.MEDIA_ROOT, 'product_images')
        file_names = os.listdir(folder_path)

        # Create a list to store the paths of similar images
        similar_images = []
        mostsimilar = []
        halfsimilar = []
        # Iterate through each image and perform image processing
        for file_name in file_names:
            img_path = os.path.join(folder_path, file_name)
            img2 = cv2.imread(img_path)
            # Resize the image to the same size as the uploaded image
            img2 = cv2.resize(img2, (img.shape[1], img.shape[0]))
            # Convert image from BGR to RGB
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

           #Compare the processed uploaded image and img2
            #and check similarity percentage

            result_score = is_similar(img,img2)
            if result_score==1:

                mostsimilar.append(img_path)

            elif result_score==2:
                print("half similar")
                halfsimilar.append(img_path)

            else:
                print("Nothing is similar")

        for image_path in mostsimilar:
            head_path = os.path.split(image_path)

        #list to store results
        MostSimilarProducts = set()
        HalfSimilarProducts = set()

        #get all products
        products = Product.objects.all()

        #for most similar products
        for product in products:
            ProductImage = PImage.objects.filter(Product=product)
            for ProductImages in ProductImage:
                for image_path in mostsimilar:
                    head_path = os.path.split(image_path)
                    imagepath = os.path.join("Product_Images/",head_path[1])
                    if ProductImages.Product_Image == imagepath:
                        print("True")
                        MostSimilarProducts.add(product)
                        break

        #for half similar product
        for hproduct in products:
            HSProductImage = PImage.objects.filter(Product=hproduct)
            for HSProductImages in HSProductImage:
                for himage_path in halfsimilar:
                    hshead_path = os.path.split(himage_path)
                    hsimagepath = os.path.join("Product_Images/", hshead_path[1])
                    if HSProductImages.Product_Image == hsimagepath:
                        print("True")
                        HalfSimilarProducts.add(hproduct)
                        break

        HalfSimilarProducts = HalfSimilarProducts - MostSimilarProducts  # remove the common products
        MostSimilarProducts = list(MostSimilarProducts)  # convert back to a list
        HalfSimilarProducts = list(HalfSimilarProducts)  # convert back to a list
        print(MostSimilarProducts)
        print(HalfSimilarProducts)

        productImages = {}
        for products in MostSimilarProducts:
            FProductImage = PImage.objects.filter(Product=products).values().first()
            productImages[products.id] = FProductImage

        hsproductImages = {}
        for hproducts in HalfSimilarProducts:
            HProductImage = PImage.objects.filter(Product=hproducts).values().first()
            hsproductImages[hproducts.id] = HProductImage

        print(productImages)
        print(hsproductImages)
        params = {'product': MostSimilarProducts,'hsproduct':HalfSimilarProducts ,"PImage": productImages,"HPImage":hsproductImages}


        return render(request,"products_result.html",params)
    return render(request,"index.html")

def is_similar(img1, img2):
    # Compare the two images and return True if they are similar,
    # otherwise return False
    img1 = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2GRAY)
    img2 = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2GRAY)
    score, _ = ssim(img1, img2, full=True)

    if score >= 0.8:
        return 1
    elif score >= 0.6 and score < 0.8:
        return 2
    else:
        return 0



# def is_similar(img1, img2, threshold=0.8):
#     # Compare the two images and return True if they are similar,
#     # otherwise return False
#     img1 = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2GRAY)
#     img2 = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2GRAY)
#     score, _ = ssim(img1, img2, full=True)
#     if score >= threshold:
#         return True
#     else:
#         return False

 #if is_similar(img, img2):
        #         similar_images.append(img_path)
        #         print("Yes image is similar")
        # print(similar_images)
        #Do something here