from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^register/', views.register, name='register'),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.account, name='account'),
    url(r'^sell/', views.sell, name='sell'),
    url(r'^book/(?P<book_id>[0-9]+)/$', views.book, name='book'),
    url(r'^search/', views.search, name="search"),
    url(r'^booktype/(?P<booktype_id>[0-9]+)/$', views.booktype, name='booktype'),
    url(r'^booksforsale/(?P<user_id>[0-9]+)/$', views.books_for_sale, name='books_for_sale'),
    url(r'^wishlist/', views.wishlist, name='wishlist'),
]