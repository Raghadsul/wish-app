from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('process', views.register),
    path('login', views.login),
    path('wishes', views.dashboard),
    path('wishes/new', views.newWish),
    path('wishes/remove/<int:wish_id>', views.removeWish),
    path('wishes/edit/<int:wish_id>', views.editWish),
    path('wishes/stats', views.stats),
    path('like/<int:wish_id>', views.like),
    path('granded/<int:wish_id>', views.granted),
    path('logout', views.logout)
]