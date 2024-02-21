import uuid
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail

from base.emails import send_account_activation_email

from .models import Profile

# Create your views here.
from django.db import transaction

@transaction.atomic
def signup_user(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
    
        user_obj = User.objects.filter(username=email)
        if user_obj.exists():
            messages.warning(request, "User with this email already exists.")
            return HttpResponseRedirect(request.path_info)
    
        try:
            with transaction.atomic():
                user_obj = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email)
                user_obj.set_password(password)
                user_obj.save()

                # Call the receiver function manually
                email_token = str(uuid.uuid4())
                Profile.objects.create(user=user_obj, email_token=email_token)
                status = send_account_activation_email(email, email_token)

                if status:
                    messages.success(request, "An email has been sent to your email.")
                else:
                    raise Exception("Failed to send activation email")

                return HttpResponseRedirect(request.path_info)
        except Exception as e:
            messages.warning(request, f"An error occurred: {e}")
            return HttpResponseRedirect(request.path_info)

    return render(request, "accounts/signup.html")

def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
    
        user_obj = User.objects.filter(username = email)
        if not user_obj.exists():
            messages.warning(request, "User with this email doesnot exist.")
            return HttpResponseRedirect(request.path_info)

        # if not user_obj[0].is_email_verified():
        #     messages.error(request, "Your account is not verfied. Please check your email inbox.")  
        #     return HttpResponseRedirect(request.path_info)

        user = authenticate(username= email, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect('/')
        messages.error(request, "Invalid Password!")
        return HttpResponseRedirect(request.path_info)
    return render(request, "accounts/login.html")

def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token = email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse("Invalid Token")