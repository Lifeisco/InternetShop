from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from main.models import Category, Item


# Create your views here.
#  TODO если в категории всего 1 стр пагинация не отобр (completed)
#  TODO при запросе на стр, где нет товаров, его перекидывает на первую стр
#  TODO отображение страницы карзины в которую пользователь добавил продукты(возможность изменить кол-во вещей)
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
    page = int(request.GET.get("page", 1))  # Текущая страница
    neXt = page - 1
    print(page)
    items_on_page = 4  # Кол-во товаров на странице

    products = Item.objects.filter(category=category)
    page_count = len(products)//items_on_page + 1 if len(products) % items_on_page else len(products)//items_on_page  # Кол-во страниц товаров
    products = products[(page-1)*items_on_page: page*items_on_page]

    data = {
        'all_categories': Category.objects.all(),
        'category': category,
        'products': products,
        'page_count': page_count,
        'page': page + 1,
        'pages': list(range(1, page_count+1)),
        'next': neXt + 1,
        'back': page - 1
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
