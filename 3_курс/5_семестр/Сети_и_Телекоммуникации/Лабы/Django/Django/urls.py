from django.contrib import admin
from django.urls import path, re_path, include
from hello import views


user_patterns = [
    # re_path(r'(?P<name>\D+)/(?P<age>\d+)', views.user, name='user'),
    # re_path(r'(?P<name>\D+)', views.user, name='user'),
    re_path(r'^$', views.user, name='user'),
]

urlpatterns = [
    re_path(r'^about/contact', views.contact, name='contact'),
    re_path(r'^about', views.about, name='about', kwargs={'name': "Anastasia", 'age': 19}),

    re_path(r'^calculate', views.calculate, name='compute'),
    re_path(r'^optimization', views.optimization, name='minimize'),

    path('access/<int:age>', views.access, name='access'),

    path('user/', include(user_patterns)),
    path('admin/', admin.site.urls),
    re_path(r'^$', views.index, name='home'),
]
