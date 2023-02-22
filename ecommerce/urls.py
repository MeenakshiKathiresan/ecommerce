"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from homepage.views import home_view, cart_view, store_view, checkout_view, about_view, product_details_view, order_complete_view, login_view

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('store/', store_view, name="store"),
    path('cart/', cart_view, name="cart"),
    path('checkout/', checkout_view, name="checkout"),
    path('login/', login_view, name="login"),
    path('order-complete/', order_complete_view, name="order_complete"),
    path('about/', about_view, name="about"),
    path('', home_view, name="home"),
    path('products/<int:product_id>/', product_details_view, name="product_details")
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

