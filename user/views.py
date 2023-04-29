from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from app.cart import OrderdProduct
from app.models import Customer,Order,OrderItem,Product,PImage
from django.http import HttpResponse

# from .models import User


# Create your views here.
def userHome(request):
    uemail = request.COOKIES.get('User_Email',"no")
    if uemail!="no":
        uemail = request.COOKIES['User_Email']
        user = Customer.objects.filter(email=uemail)
        allorders = Order.objects.all()
        user_orderd_products = []
        for orderItem in allorders:
            for u in user:
                if orderItem.OrderDetail.CustomerOrder.email == uemail:
                    product_total = orderItem.OrderDetail.ItemQuantity * int(
                        orderItem.OrderDetail.ProductOrder.Product_Price)

                    orderedProduct = OrderdProduct(Product_id=orderItem.OrderDetail.ProductOrder.id,
                                                   Product_Name=orderItem.OrderDetail.ProductOrder.Product_Name,
                                                   Product_Price=orderItem.OrderDetail.ProductOrder.Product_Price,
                                                   Product_Category=orderItem.OrderDetail.ProductOrder.Product_Category,
                                                   Product_Description=orderItem.OrderDetail.ProductOrder.Product_Description,
                                                   Product_Stock=orderItem.OrderDetail.ProductOrder.Product_Stock,
                                                   slug=orderItem.OrderDetail.ProductOrder.slug,
                                                   Quantity=orderItem.OrderDetail.ItemQuantity,
                                                   Total=product_total,
                                                   CName=orderItem.OrderDetail.CustomerOrder.name,
                                                   CEmail=orderItem.OrderDetail.CustomerOrder.email,
                                                   CPhone=orderItem.OrderDetail.CustomerOrder.phone,
                                                   CAddress=orderItem.OrderDetail.CustomerOrder.address,
                                                   CCity=orderItem.OrderDetail.CustomerOrder.city,
                                                   CState=orderItem.OrderDetail.CustomerOrder.state,
                                                   CZipcode=orderItem.OrderDetail.CustomerOrder.zipcode,
                                                   )

                    user_orderd_products.append(orderedProduct)

        context = {
            "orders": user_orderd_products
        }
        return render(request, 'userHome.html', context)
    return render(request,'userLogin.html')
def userSignUp(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('uhome')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('uhome')

        if len(uname) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('uhome')

        if len(pass1) < 8:
            messages.error(request, "Password must be atleast 8 characters!!")
            return redirect('uhome')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('uhome')

        if not uname.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('uhome')

        my_user = User.objects.create_user(uname, email, pass1)
        my_user.save()

        messages.success(request,"Your Account Created Succesfully")

        return redirect('ulogin')
    else:
        return render(request, 'userSignUp.html')

def userLogin(request):
    if request.method == 'POST':
        uemail = request.POST.get('email')
        user = Customer.objects.filter(email=uemail)

        if user.exists():
           for u in user:
               Useremail = u.email
           response = redirect('userHome')
           response.set_cookie('User_Email',Useremail)
           return response
        else:
            messages.error(request,"Brand Credentials")
            return render(request, 'userLogin.html')

    return render(request,"userLogin.html")

def uSingOut(request):
    response = redirect('ulogin')
    response.delete_cookie('User_Email')
    return response



