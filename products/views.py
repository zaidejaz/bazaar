from django.http import HttpResponse
from django.shortcuts import render
from .models import Product, SizeVariant
# Create your views here.
def product(request, product_slug):
    try:
        product = Product.objects.get(slug = product_slug)
        context = { 'product' : product}

        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price
            
        return render(request, 'products/product.html', context)
    except Exception as e:
        return HttpResponse(e)