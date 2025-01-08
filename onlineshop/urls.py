from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from main.views import index, login_page, reg_page, log_out, view_products_by_category, cart, order, product, catalog, activate_user


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('', index, name='home'),
    path('all_products', catalog, name='catalog'),
    path('login/', login_page, name='login'),
    path('sign_up/', reg_page, name='register'),
    path('logout/', log_out, name='logout'),
    path('category/<str:category_url>/', view_products_by_category, name='view_products_by_category'),
    path('cart/', cart, name='cart'),
    path('order/', order, name='order'),
    path('product/', product, name='product'),
    path('activate_user/', activate_user, name='activate_user')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

