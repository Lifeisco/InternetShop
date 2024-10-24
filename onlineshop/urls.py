"""
URL configuration for onlineshop project.

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
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from main.views import index, login_page, reg_page, log_out, view_products_by_category, card

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('home/', index, name='home'),
    path('login/', login_page, name='login'),
    path('sign_up/', reg_page, name='register'),
    path('logout/', log_out, name='logout'),
    path('category/<str:category_name>/', view_products_by_category, name='view_products_by_category'),
    path('card/', card, name='card')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
