"""
URL configuration for store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from products.views import *
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)
router1 = routers.SimpleRouter()
router1.register(r'categories', CategoriesViewSet)






urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/basket', BasketAPIView.as_view()),
    path('api/v1/', include(router1.urls)),
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('products/', include('products.urls', namespace='products')),
    path('users/', include('users.urls', namespace='users')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)