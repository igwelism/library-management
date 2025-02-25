from django.contrib import admin

from .models import Book, Loan


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "stock", "created_at", "updated_at")
    list_filter = ("author", "created_at", "updated_at")
    search_fields = ("title", "author")
    date_hierarchy = "created_at"
    ordering = ("author", "created_at")
    readonly_fields = ("created_at", "updated_at")


class LoanAdmin(admin.ModelAdmin):
    list_display = (
        "borrower__email",
        "book__title",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "created_at", "updated_at")
    search_fields = ("borrower__name", "book__title")
    date_hierarchy = "created_at"
    autocomplete_fields = ("borrower", "book")
    ordering = ("book__title", "created_at")
    readonly_fields = ("status", "fine", "return_date", "created_at", "updated_at")


admin.site.register(Book, BookAdmin)
admin.site.register(Loan, LoanAdmin)
