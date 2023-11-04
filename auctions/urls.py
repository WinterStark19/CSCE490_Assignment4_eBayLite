from django.urls import path

from auctions import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("showcategory/", views.showcategory, name="showcategory"),
    path('categories/', views.categories, name='categories'),
    path("listings/<int:id>", views.listings, name="listings")
]
