from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("search/", views.BookSearchView.as_view(), name="search"),
    path("loan/book/<int:pk>", views.UserLoanBookView.as_view(), name="loan"),
    path("user/loan/", views.LoanBookView.as_view(), name="user-loan"),
]
