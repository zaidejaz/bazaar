from django.urls import path
from .views import login_user, signup_user, activate_email

urlpatterns = [
    path('login/', login_user, name="login_user"),
    path('signup/', signup_user, name="signup_user"),
    path('activate/<str:email_token>/', activate_email, name="activate_email"),
]
