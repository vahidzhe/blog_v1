from django.urls import path
from . views import *
urlpatterns = [
    path("create/",post_create, name="create"),
    path("detail/<slug:slug>",post_detail, name="detail"),
    path("update/<slug:slug>",post_update, name="update"),
    path("delete/<slug:slug>",post_delete, name="delete"),
    path("add_child_comment/<int:id>/",add_child_comment, name="add_child_comment"),

]