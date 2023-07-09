from django.urls import path

from . import views

urlpatterns = [
    path('post-table', views.PostTableView.as_view()),
]