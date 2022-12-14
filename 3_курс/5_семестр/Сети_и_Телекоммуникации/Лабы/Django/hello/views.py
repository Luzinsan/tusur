from django.shortcuts import render
from datetime import datetime
from django.template.response import TemplateResponse
from .forms import UserForm

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, \
    HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder


# установка куки
def set(request):
    # получаем из строки запроса имя пользователя
    username = request.GET.get("username", "Undefined")
    # создаем объект ответа
    response = HttpResponse(f"Hello {username}")
    # передаем его в куки
    response.set_cookie("username", username)
    return response


# получение куки
def get(request):
    # получаем куки с ключом username
    username = request.COOKIES['username']
    return HttpResponse(f"Hello {username}")


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
    data = {"header": "Hello Django", "message": "Welcome to Python"}
    return render(request, "index.html", context=data)


def user(request):
    header = "Данные пользователя"  # обычная переменная
    if request.method == "POST":
        userform = UserForm(request.POST)
        if userform.is_valid():
            # langs = userform.cleaned_data['languages']
            name = userform.cleaned_data['name']
            age = userform.cleaned_data['age']
            return HttpResponse(f"""<div>Name: {name}</div>
                                    <div>Age: {age}</div>""")
                                    # <div>Languages: {langs}</div>""")
        else:
            return HttpResponseBadRequest("Invalid data")
    else:
        # userform = UserForm(field_order=["date", "name", "email", "password", "comment"])
        userform = UserForm()
        date = datetime.now()
        address = ("Абрикосовая", 23, 45)  # кортеж
        optimize = Minimize('Newton', 'x+1')
        colors = {"red": 'красный', "green": 'зелёный', "blue": 'синий'}
        data = {"header": header, "address": address, "optimize": optimize, "colors": colors,
                "date": date, "form": userform}
        return TemplateResponse(request, "user.html", context=data)



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
    return TemplateResponse(request,  "calculate.html")


def optimization(request):
    min = Minimize("Newton", 1)
    return JsonResponse(min, safe=False, encoder=MinimizeEncoder)


class Minimize:
    def __init__(self, method, function):
        self.method = method
        self.function = function


class MinimizeEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Minimize):
            return {"method": obj.method, "function": obj.function}
            # return obj.__dict__
        return super().default(obj)
