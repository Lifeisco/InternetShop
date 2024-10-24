from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from main.models import Category, Item


# Create your views here.
#  TODO пагинацию для вывода каталога товаров
#  TODO запрашивать только часть товаров, отображаемых на странице(гуглить django orm limit)
#  TODO отображение страницы карзины в которую пользователь добавил продукты(возможность изменить кол-во вещей)
#  TODO кнопка 'Оформить закать' -> корзина опустошается -> создается объект заказа


def index(request):
    data = {
        'categories': Category.objects.all()
    }
    return render(request, 'main/index.html', context=data)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)  # Сама проверка, есть ли пользователь в БД

        if user is not None:
            login(request, user)
            request.session['card'] = []
            return redirect('/home')
        else:
            error_message = 'Неверное имя пользователя или пароль'

    return render(request, 'main/log_in.html')


def reg_page(request):
    if request.method == 'POST':
        new_user = User.objects.create_user(request.POST.get("name"), request.POST.get("email"), request.POST.get("password"))
        new_user.save()

    return render(request, 'main/register.html')


def log_out(request):
    logout(request)
    return redirect('/')


def view_products_by_category(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    print(category)
    products = Item.objects.filter(category=category)
    data = {
        'categories': category,
        'products': products
    }
    return render(request, 'main/Category.html', context=data)


def card(request):
    data = request.session.get('card', [])
    if request.method == 'GET':
        product = request.GET.get('product', False)
        if product:
            request.session['card'].append({'id': product,
                                            'amount': 1})
    return render(request, 'main/card.html', context=data)
