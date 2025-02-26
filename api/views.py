from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404

from library.models import Loan
from .serializers import LoanSerializer
from .pagination import ListPagination


class LoanListAPIView(generics.ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    pagination_class = ListPagination


class LoanCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        loan_instance = Loan.objects.filter(
            borrower=request.data.get("borrower"), book=request.data.get("book")
        ).first()

        if loan_instance:
            serializer = LoanSerializer(loan_instance, data=request.data)
        else:
            serializer = LoanSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Loan
    serializer_class = LoanSerializer


class LoanUpdateAPIView(generics.UpdateAPIView):
    def put(self, request, *args, **kwargs):
        loan_instance = get_object_or_404(
            Loan,
            borrower=request.data.get("borrower"),
            book=request.data.get("book"),
            pk=kwargs.get("pk"),
        )
        serializer = LoanSerializer(loan_instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
