from django.shortcuts import redirect, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from accounting.api.serializers import (
    BalanceSheetItemSerializer,
    BalanceGroupSerializer,
    AccountSerializer,
    TransactionSerializer,
)
from accounting.models import BalanceSheetItem, BalanceGroup, Account, Transaction


class BalanceSheetItemView(viewsets.ModelViewSet):
    """
    Статьи баланса:
    - список / одна статья
    - get, post, put, patch, delete
    """

    serializer_class = BalanceSheetItemSerializer
    queryset = BalanceSheetItem.objects.all()


class BalanceGroupView(viewsets.ModelViewSet):
    """
    Балансовые группы:
    - список / одна группа
    - get, post, put, patch, delete
    """

    serializer_class = BalanceGroupSerializer
    queryset = BalanceGroup.objects.all()


class AccountView(viewsets.ModelViewSet):
    """
    Счета:
    - список / один счёт
    - get, post, put, patch, delete
    """

    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class TransactionView(viewsets.ModelViewSet):
    """
    Транзакции:
    - список, одна транзакция
    - get, post, put, patch, delete
    """

    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    # TODO: delete transactions apiview, expand modelviewset with extra [post]


class AccountsListView(APIView):
    """
    Счёты:
        Список
    """

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "accounts_list.html"
    serializer_class = AccountSerializer

    def get(self, request):
        accounts = Account.objects.all()

        if request.accepted_renderer.format == "html":
            return Response({"accounts": accounts})
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)


class TransactionCreateView(APIView):
    """
    Создание транзакции:
        Форма выбора
    """

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "transaction_creating.html"
    serializer_class = TransactionSerializer

    def get(self, request):
        accounts = Account.objects.all()
        return Response({"accounts": accounts})

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("transactions-create")
        accounts = Account.objects.all()
        print(serializer.errors)
        return Response({"accounts": accounts, "errors": serializer.errors})


class TransactionHistoryView(APIView):
    """
    История транзакций:
        Список
    """

    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "transaction_history.html"

    def get(self, request):
        transactions = Transaction.objects.all()
        return Response({"transactions": transactions})


class TransactionVoidView(APIView):
    """
    Аннулирование транзакции
        post: /transactions/<id>/void/
    """

    def post(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)
        if transaction.is_voided:
            return Response(
                {"error": "Transaction already voided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            transaction.voided()
            return Response(
                {"success": f"Transaction #{transaction.pk} voided successfully"}
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
