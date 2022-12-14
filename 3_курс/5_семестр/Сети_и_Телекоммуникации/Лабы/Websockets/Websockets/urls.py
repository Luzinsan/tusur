from django.urls import path, re_path
from minimization import views

urlpatterns = [
    re_path(r'^results', views.results, name='results'),
    re_path(r'^minimization', views.minimization, name='minimization'),
    re_path(r'^user', views.user, name='user'),
    re_path(r'^$', views.index, name='home'),
]
