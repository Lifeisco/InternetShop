from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from main.models import Category, Item, Order, OrderItem, Customer
from datetime import datetime
from django.core.mail import send_mail
import hashlib

from onlineshop import settings


def index(request):
    return render(request, 'main/index.html')

def catalog(request):
    data = {
        'products': Item.objects.all(),
        'all_categories': Category.objects.all()
    }
    return render(request, 'main/catalog.html', context=data)

# Страница конкретного товара с его описанием и т.д.
def product(request):
    product_id = request.GET.get('id', False)
    # сообщение об ошибке
    if (not product_id or
            not product_id.isdigit() or
            not Item.objects.filter(id=product_id).exists()):
        data = {'item': False}
        return render(request, 'main/product.html', context=data)
    item = Item.objects.get(id=product_id)
    data = {'item': item,
            'all_categories': Category.objects.all()}

    return render(request, 'main/product.html', context=data)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)  # Проверка, на пользователя в БД
        #  TODO если юзер не активен, сообщаем ему код активации по емаил
        if user is not None:
            login(request, user)
            request.session['cart'] = {}
            return redirect('/')
        else:
            error_message = 'Неверное имя пользователя или пароль'
    data = {'all_categories': Category.objects.all()}

    return render(request, 'main/log_in.html', context=data)


def reg_page(request):

    hash_code = ''
    if request.method == 'POST':
        new_user = User.objects.create_user(request.POST.get("name"),
                                            request.POST.get("email"),
                                            request.POST.get("password")
                                            )
        new_user.is_active = False
        new_user.save()
        hash_code = hashlib.md5(f'{new_user.username}{new_user.id}'.encode()).hexdigest()
        #  TODO усложнить код(добавить еще id для геню. кода)
        subject = new_user.username
        message = (f'Привет {subject}! Рады видеть!\nПерейдите по ссылке, чтобы подтвердить ваш email адрес: '
                   f'http://127.0.0.1:8000/activate_user/?code={hash_code}&user={subject}')
        from_email = settings.EMAIL_HOST_USER
        to_email = new_user.email
        send_mail(
            subject, # Имя пользователя
            message, # Сообщение в email письме
            from_email, # От кого пересылаем
            [to_email], # email пользователя
            fail_silently=False,
        )
        Customer.objects.create(user=new_user).save()
    data = {'all_categories': Category.objects.all(),
            'code': hash_code}

    return render(request, 'main/register.html', context=data)

def activate_user(request):
    code = request.GET.get("code", default='')
    username = request.GET.get("user", default='')

    user = User.objects.get(username=username)

    hash_code = hashlib.md5(f'{username}{user.id}'.encode()).hexdigest()
    #  TODO усложнить код(добавить еще id для геню. кода) тут тоже

    print(f'hash_code - {hash_code}\ncode - {code}')

    if code == hash_code:
        mess = "Вы успешно прошли регистрацию! Теперь ваш аккаунт активен"
        user = User.objects.get(username=username)
        user.is_active = True # Активация пользователя
        user.save()
    else:
        mess = "Что то пошло не так, попробуйте снова"


    data = {
        'message': mess
    }
    return render(request, 'main/activating.html', context=data)

def log_out(request):
    logout(request)
    return redirect('/')


def view_products_by_category(request, category_url):
    search = request.GET.get("search", '')
    page = int(request.GET.get("page", 1))  # Текущая страница
    neXt = page - 1
    items_on_page = 4  # Кол-во товаров на странице

    if category_url == 'all':
        category = 'all'
        if search:
            products = Item.objects.filter(name__contains=search)
            search = f'search={search}&'
            print(search)
        else:
            products = Item.objects.all()
    else:
        category = get_object_or_404(Category, url=category_url)
        if search:
            products = Item.objects.filter(category=category, name__contains=search)
        else:
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
        'back': page - 1,
        'search': search}
    return render(request, 'main/category.html', context=data)


def cart(request):

    carT = dict(request.session.get('cart', {}))
    if request.method == 'POST':
        product = request.POST.get('product', False)
        action = request.POST.get('action', False)
        if product and action == 'add':
            carT[product] = 1
        elif product and action == 'delete':
            if product in carT:
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
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        if request.method == 'POST':
            action = request.POST.get('action', False)
            if action == 'make_order':
                carT = dict(request.session.get('cart', {}))
                if carT != {}:

                    products_id = [x for x in carT]
                    product = Item.objects.filter(id__in=products_id)
                    total_price = 0
                    for i in range(len(product)):
                        total_price += product[i].price * carT[str(product[i].id)]

                    obj_order = Order.objects.create(customer=customer, created_date=datetime.now(),
                                                         status='Pending', total_price=total_price)

                    for i in range(len(product)):
                        OrderItem.objects.create(order=obj_order, product=product[i], quantity=carT[str(product[i].id)],
                                                 price=product[i].price * carT[str(product[i].id)])

                    carT = {}
                    request.session['cart'] = carT #  опустошение корзины

        order_id = request.GET.get('id', False)
        all_orders = False
        if order_id == 'all':
            obj_order = Order.objects.filter(customer=customer)
            all_orders = True
        elif str(order_id).isdigit():
            obj_order = Order.objects.filter(customer=customer, id=order_id).last()
        else:
            obj_order = Order.objects.filter(customer=customer).last()

    else:
        data = {'error_message': 'Авторизуйтесь или зарегистрируйтесь, чтобы заказать'}
        return render(request, 'main/order.html', context=data)

    data = {
        'obj_order': obj_order,
        'products_list': OrderItem.objects.filter(order=obj_order) if not all_orders else False,
        'all_categories': Category.objects.all(),
        'all_orders': all_orders
    }

    return render(request, 'main/order.html', context=data)
