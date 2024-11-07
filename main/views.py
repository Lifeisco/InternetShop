from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from main.models import Category, Item, Order


#  TODO кнопка 'Оформить закать' -> корзина опустошается -> создается объект заказа

def index(request):
    data = {
        'all_categories': Category.objects.all()
    }
    return render(request, 'main/index.html', context=data)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)  # Проверка, на пользователя в БД

        if user is not None:
            login(request, user)
            request.session['cart'] = {}
            return redirect('/')
        else:
            error_message = 'Неверное имя пользователя или пароль'

    return render(request, 'main/log_in.html')


def reg_page(request):
    if request.method == 'POST':
        new_user = User.objects.create_user(request.POST.get("name"),
                                            request.POST.get("email"),
                                            request.POST.get("password"))
        new_user.save()

    return render(request, 'main/register.html')


def log_out(request):
    logout(request)
    return redirect('/')


def view_products_by_category(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    page = int(request.GET.get("page", 1))  # Текущая страница
    neXt = page - 1
    items_on_page = 4  # Кол-во товаров на странице

    products = Item.objects.filter(category=category)
    page_count = len(products)//items_on_page + 1 if len(products) % items_on_page else len(products)//items_on_page
    # Кол-во страниц товаров
    if not 0 < page < page_count and page != page_count:
        page = 1
        neXt = 0
    products = products[(page-1)*items_on_page: page*items_on_page]

    data = {
        'all_categories': Category.objects.all(),
        'category': category,
        'products': products,
        'page_count': page_count,
        'page': page + 1,
        'next': neXt + 1,
        'back': page - 1
    }
    return render(request, 'main/category.html', context=data)


def cart(request):

    carT = dict(request.session.get('cart', {}))
    if request.method == 'POST':
        product = request.POST.get('product', False)
        action = request.POST.get('action', False)
        if product and action == 'add':
            carT[product] = 1
        elif product and action == 'delete':
            del carT[product]

        elif product and action == 'increment':
            amount = int(request.POST.get('amount', 1))

            carT[product] += amount
            if carT[product] <= 0:
                del carT[product]

        elif action == 'delete_all_from_cart':
            carT = {}
            request.session['cart'] = carT

        request.session['cart'] = carT
    products_id = [x for x in carT]
    product = Item.objects.filter(id__in=products_id)
    total_price = 0
    for i in range(len(product)):
        product[i].amount = carT[str(product[i].id)]
        product[i].total_price = product[i].amount * product[i].price
        total_price += product[i].total_price
    data = {
        'total_price': total_price,
        'cart': carT,
        'products': product,
        'all_categories': Category.objects.all()
    }
    return render(request, 'main/cart.html', context=data)


def order(request):
    if request.method == 'POST':
        carT = dict(request.session.get('cart', {}))
        object_of_order = Order.objects.create()
    data = {

    }
    return render(request, 'main/order.html', context=data)
