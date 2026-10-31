from django.urls import path
from . import views


urlpatterns = [

    path('', views.home, name='home'),

    path('article/<int:pk>/',
         views.article_detail,
         name='article_detail'),

    path('article/create/',
         views.article_create,
         name='article_create'),

    path('article/<int:pk>/edit/',
         views.article_edit,
         name='article_edit'),

    path('article/<int:pk>/delete/',
         views.article_delete,
         name='article_delete'),

    path('register/',
         views.register,
         name='register'),

    path('login/',
         views.user_login,
         name='login'),

    path('logout/',
         views.user_logout,
         name='logout'),

]
