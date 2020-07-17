from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('all_users', views.all_users),
    path('register', views.create),
    path('login', views.login),
    path('<int:user_id>/delete', views.delete),
    path('main', views.main),
    path('logout', views.logout),
    path('new_book', views.new_book),
    path('show_book/<int:book_id>', views.show_book),
    path('like_book/<int:book_id>', views.like_book),
    path('unlike_book/<int:book_id>' , views.unlike_book),
    path('edit/<int:book_id>', views.edit),
    path('update/<int:book_id>', views.update)
]