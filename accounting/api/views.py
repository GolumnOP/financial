from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from accounting.api.serializers import (
    BalanceSheetItemSerializer,
    BalanceGroupSerializer,
    AccountSerializer,
)
from accounting.models import BalanceSheetItem, BalanceGroup, Account


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

# class TransactionView(APIView):
#     def get(self, request):
#         return ...
#
#     def delete(self, request):
#         # voided?
#         return ...



# 🧾 Интерфейс (ниже описаны страницы)
# •	Список счетов: отображение всех счетов с текущими балансами
# •	Создание транзакции: форма с выбором счетов и суммой
# •	История транзакций: таблица с датой, описанием, суммой, дебетом и кредитом


class AccountsListView(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = "accounts_list.html"
    serializer_class = AccountSerializer

    def get(self, request):
        accounts = Account.objects.all()

        if request.accepted_renderer.format == "html":
            return Response({"accounts": accounts})
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)