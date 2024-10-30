from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from main.models import Category, Item


#  TODO если в категории всего 1 стр пагинация не отобр (completed)
#  TODO при запросе на стр, где нет товаров, его перекидывает на первую стр (работает)
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

        user = authenticate(request, username=username, password=password)  # Проверка, на пользователя в БД

        if user is not None:
            login(request, user)
            request.session['cart'] = []
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
    carT = request.session.get('cart', [])
    if request.method == 'POST':
        product = request.POST.get('product', False)
        action = request.POST.get('action', False)
        if product and action == 'add':
            request.session['cart'].append({'id': product, 'amount': 1})
        elif product and action == 'delete':
            pass  # TODO удаление из корзины товара по ид
        elif product and action == 'increment':
            amount = request.POST.get('amount', 1)
            # TODO увеличение кол-во товара на amount

    products_id = [x['id'] for x in carT]
    product = Item.objects.filter(id__in=products_id)

    data = {
        'products': product
    }
    return render(request, 'main/cart.html', context=data)
