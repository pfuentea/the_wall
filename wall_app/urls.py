from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path('wall', views.wall),
    path('login', views.login),
    path('logout', views.logout),
    path('register', views.register),
    path('message/new', views.message_new),
    path('comentario/new', views.comentario_new),

]
