from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, \
    HttpResponseBadRequest, HttpResponseForbidden


def index(request):
    scheme = request.scheme  # схема запроса (http или https)
    body = request.body  # представляет тело запроса в виде строки байтов
    path = request.path  # получаем запрошенный путь
    method = request.method  # метод запроса (GET, POST, PUT и т.д.)
    encoding = request.encoding  # кодировка
    content_type = request.content_type  # тип содержимого запроса (значение заголовка CONTENT_TYPE)
    host = request.META["HTTP_HOST"]  # получаем адрес сервера
    user_agent = request.META["HTTP_USER_AGENT"]  # получаем данные бразера

    return HttpResponse(f"""
        <b>Главная</b>
        <p>Схема запроса: {scheme}</p>
        <p>Тело запроса: {body}</p>
        <p>Запрошенный путь: {path}</p>
        <p>Метод запроса (GET, POST, PUT и т.д.): {method}</p>
        <p>Кодировка: {encoding}</p>
        <p>Тип содержимого запроса (значение заголовка CONTENT_TYPE): {content_type}</p>
        <p>Host: {host}</p>
        <p>User-agent: {user_agent}</p>
    """, headers={"SecretCode": "21234567"})


def about(request, name, age):
    return HttpResponse(f"""
            <h2>О пользователе</h2>
            <p>Имя: {name}</p>
            <p>Возраст: {age}</p>
    """)


def contact(request):
    return HttpResponse("<b>Контакты</b>")


def user(request):
    name = request.GET.get('name', "Undefined")
    age = request.GET.get('age', None)
    return HttpResponse(f"""
    <h1>Информация о пользователе</h1>
    <p>Имя: {name}</p>
    <p>Возраст: {age}</p>    
    """)


def access(request, age):
    # если возраст НЕ входит в диапазон 1-110, посылаем ошибку 400
    if age not in range(1, 111):
        print(age+1)
        return HttpResponseBadRequest("Некорректные данные")
    # если возраст больше 17, то доступ разрешен
    if (age > 17):
        return HttpResponse("Доступ разрешен")
    # если нет, то возвращаем ошибку 403
    else:
        return HttpResponseForbidden("Доступ заблокирован: недостаточно лет")


def calculate(request):
    return HttpResponseRedirect('/')


def optimization(request):
    return HttpResponsePermanentRedirect('/')
