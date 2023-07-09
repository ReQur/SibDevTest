from django.urls import path

from . import views

urlpatterns = [
    path("table", views.PostTableView.as_view()),
    path("spenders", views.GetTopCustomers.as_view()),
]
