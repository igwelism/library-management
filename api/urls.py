from django.urls import path

from . import views

urlpatterns = [
    path("loan/book/", views.LoanCreateAPIView.as_view(), name="create_loan"),
    path("loans/", views.LoanListAPIView.as_view(), name="list_loan"),
    path(
        "loan/<int:pk>/",
        views.LoanRetrieveAPIView.as_view(),
        name="get_loan",
    ),
    path(
        "update/loan/<int:pk>/",
        views.LoanUpdateAPIView.as_view(),
        name="update_loan",
    ),
]
