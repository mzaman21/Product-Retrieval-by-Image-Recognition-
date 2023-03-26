from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse

# from .models import User


# Create your views here.
def userHome(request):
    return render(request,"userHome.html")

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
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            context={
                'user_name':user.username
            }
            return render(request,'userHome.html',context)

        else:
            messages.error(request,"Username or Password is incorrect!!!")
            return redirect('uhome')

    else:
        return render(request,"userLogin.html")

def uSingOut(request):
    logout(request)
    return redirect('ulogin')



