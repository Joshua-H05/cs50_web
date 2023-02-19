from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page_name>", views.page_search, name="wiki"),
    path("search", views.search, name="search"),
    path("random/", views.random_page, name="random_page"),
    path("new/", views.new_page, name="new_page"),
    path("wiki/<str:name>/edit", views.edit_page, name="edit"),
]