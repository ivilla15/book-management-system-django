from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='index'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('shoppingcart', views.shopping_cart, name='shoppingcart'),
    path('cart_remove/<int:book_id>',views.cart_remove, name='cart_remove'),
    path('cart_add/<int:book_id>', views.cart_add, name='cart_add'),
    path('aboutus', views.about_us, name='about_us'),
    path('favorites', views.favorites, name='favorites'),
    path('favorites_remove/<int:book_id>',views.favorites_remove, name='favorites_remove'),
    path('favorites_add/<int:book_id>', views.favorites_add, name='favorites_add'),
    path('search/', views.search_books, name='search_books'),
]

