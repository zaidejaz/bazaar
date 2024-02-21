from django.urls import path
from .views import product

urlpatterns = [
    path('product/<product_slug>', product, name="get_product"),
]

