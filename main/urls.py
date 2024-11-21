from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),
    path('history', views.history, name='history'),
    path('entry', views.entry, name='entry'),
    path('team', views.team, name='team'),
    path('registration', views.registration, name='registration'),
    path('shop', views.shop, name='shop'),
    path('test', views.test, name='test'),
    path('postuser', views.postuser, name='postuser'),
    path('postuserentry', views.postuserentry, name='postuserentry'),
    path('loggout', views.loggout, name='loggout'),
    path('lk', views.lk, name='lk'),
    path('newtovar', views.newtovar, name='newtovar'),
    path('deltovar/<int:prod_id>/', views.deltovar, name='deltovar'),
    path('changerole', views.changerole, name='changerole'),
    path('vkorzinu/<int:prod_id>/', views.vkorzinu, name='vkorzinu'),
    path('trashbox', views.trashbox, name='trashbox'),
    path('deltovartrash/<int:prod_id>/', views.deltovartrash, name='deltovartrash'),
    path('makesell', views.makesell, name='makesell'),
    path('tovar/<int:prod_id>/', views.tovar, name='tovar'),
    path('previos/<int:prod_id>/', views.previos, name='previos'),
    path('next/<int:prod_id>/', views.next, name='next'),
    path('homep', views.homep, name='homep'),
]
