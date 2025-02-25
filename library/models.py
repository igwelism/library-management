from datetime import datetime, timedelta

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import F

from common.models import AbstractModel
from accounts.models import CustomUser


class Book(AbstractModel):
    class BookCategory(models.TextChoices):
        EDUCATION = "education", _("Education")
        ENTERTAINMENT = "entertainment", _("Entertainment")
        COMICS = "comics", _("Comics")
        BIOGRAPHY = "biography", _("Biography")
        HISTORY = "history", _("History")

    title = models.CharField(_("Title"), max_length=100)
    isbn = models.CharField(_("ISBN"), max_length=13)
    author = models.CharField(_("Book Author"), max_length=40)
    page_count = models.PositiveIntegerField(_("Number of Pages"))
    is_available = models.BooleanField(_("Is Available"))
    stock = models.PositiveIntegerField(_("Copies Left"))
    category = models.CharField(
        max_length=20, choices=BookCategory.choices, default=BookCategory.EDUCATION
    )

    def __str__(self):
        return str(self.title) + "[" + str(self.isbn) + "]"

    def save(self, *args, **kwargs):
        self.is_available = True if self.stock != 0 else False
        super().save(*args, **kwargs)

    class Meta(AbstractModel.Meta):
        unique_together = ("title", "isbn")


def get_expiry():
    return datetime.today() + timedelta(days=15)


class Loan(AbstractModel):
    class Status(models.TextChoices):
        BORROWED = "borrowed", _("Borrowed")
        LOST = "lost", _("LOST")
        RETURNED = "returned", _("Returned")

    borrower = models.ForeignKey(
        CustomUser,
        verbose_name=_("Borrower"),
        related_name="loans",
        on_delete=models.CASCADE,
    )
    book = models.ForeignKey(
        Book,
        verbose_name=_("book"),
        related_name="loans",
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.BORROWED
    )
    borrowed_date = models.DateField(_("Borrowed Date"), auto_now=True)
    expected_return_date = models.DateField(_("Return Due Date"), default=get_expiry)
    return_date = models.DateField(_("Returned Date"), null=True, blank=True)
    fine = models.DecimalField(
        _("Late Return Charge"), max_digits=5, decimal_places=2, default=0.0
    )

    def __str__(self):
        return str(self.borrower.name) + "[" + str(self.book.title) + "]"

    def save(self, *args, **kwargs):
        if self.book.stock > 0:
            existing_loan = Loan.objects.filter(pk=self.id).first()
            status_value = existing_loan.status if existing_loan else None

            if self.status == "borrowed" and self.status != status_value:
                self.book.stock = F("stock") - 1
            elif self.status == "returned" and self.status != status_value:
                self.book.stock = F("stock") + 1

        self.book.save(update_fields=["stock"])
        super().save(*args, **kwargs)

    class Meta(AbstractModel.Meta):
        unique_together = ("borrower", "book")
