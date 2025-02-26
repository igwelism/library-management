from django.http import HttpResponseRedirect
from django.views import generic
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse


from .models import Book, Loan


class HomePageView(generic.ListView):
    model = Book
    paginate_by = 10
    template_name = "home.html"


class BookSearchView(generic.ListView):
    model = Book
    paginate_by = 10
    template_name = "home.html"

    def get_queryset(self):
        search_query = self.request.GET.get("query").strip()

        return Book.objects.filter(
            Q(title__icontains=search_query) | Q(author__icontains=search_query)
        )


class UserLoanBookView(generic.View):
    def get(self, request, *args, **kwargs):
        book_object = get_object_or_404(Book, pk=kwargs.get("pk"))

        # get or create loan instance
        loan, created = Loan.objects.get_or_create(
            borrower=request.user,
            book=book_object,
        )

        if not created:
            loan.status = "borrowed"
            loan.save()

        return HttpResponseRedirect(reverse("user-loan"))


class LoanBookView(generic.ListView):
    template_name = "borrowed.html"
    paginate_by = 10

    def get_queryset(self):
        return Loan.objects.filter(borrower=self.request.user)
