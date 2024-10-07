from django.shortcuts import render, HttpResponseRedirect
from rest_framework.views import APIView

from products.models import Product, ProductCategory, Basket
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from rest_framework import generics, viewsets
from rest_framework.response import Response
from products.serializers import ProductSerializer, CategoriesSerializer, BasketSerializer


def index(request):
    context = {'title': 'Store'}
    return render(request, 'products/index.html', context)

def products(request, category_id=None, page_number=1):

    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()

    per_page = 3
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)

    context = {
        'title': 'Products',
        'products': products_paginator,
        'categories': ProductCategory.objects.all()
    }

    return render(request, 'products/products.html', context)

@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])



class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = CategoriesSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BasketAPIView(APIView):
    def get(self, request):
        w = Basket.objects.all()
        return Response({'basket': BasketSerializer(w, many=True).data})

    def post(self, request):
        product_id = request.data.get('id')
        if request.data.get('act') == 'delete':
            basket = Basket.objects.get(product=product_id)
            print(basket.quantity)
            if basket.quantity > 1:
                basket.quantity -= 1

                basket.save()
            else:
                basket.delete()
            return Response({'success': f'Product {product_id} deleted from basket'})
        else:


            product = Product.objects.get(id=product_id)
            baskets = Basket.objects.filter(user=request.user, product=product)

            if not baskets.exists():
                Basket.objects.create(user=request.user, product=product, quantity=1)
            else:
                basket = baskets.first()
                basket.quantity += 1
                basket.save()
            return Response({'success': f'Product {product_id} added to basket'})
