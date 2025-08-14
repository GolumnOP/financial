from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from accounting.models import (
    # Transaction,
    Account,
    BalanceGroup,
    BalanceSheetItem,
)

class BalanceSheetItemSerializer(serializers.Serializer):
    class Meta:
        model = BalanceSheetItem
        fields = ["id", "name"]


class BalanceGroupSerializer(serializers.Serializer):
    balance_sheet_item = BalanceSheetItemSerializer(read_only=True)
    balance_sheet_item_id = serializers.PrimaryKeyRelatedField(
        queryset=BalanceSheetItem.objects.all(),
        write_only=True,
        source="balance_sheet_item",
    )

    class Meta:
        model = BalanceGroup
        fields = ["id", "name", "balance_sheet", "balance_sheet_id"]


class AccountSerializer(serializers.Serializer):
    balance_group = BalanceGroupSerializer(read_only=True)
    balance_group_id = serializers.PrimaryKeyRelatedField(
        queryset=BalanceGroup.objects.all(), write_only=True, source="balance_group"
    )

    class Meta:
        model = Account
        fields = [
            "id",
            "number",
            "name",
            "type",
            "balance_group",
            "balance_group_id",
            "balance",
        ]

# class TransactionSerializer(serializers.Serializer):
#     debit_account = AccountSerializer(read_only=True)
#     debit_account_id = serializers.PrimaryKeyRelatedField(
#         queryset=Account.objects.all(), source="debit_account"
#     )
#     credit_account = AccountSerializer(read_only=True)
#     credit_account_id = serializers.PrimaryKeyRelatedField(
#         queryset=Account.objects.all(), source="credit_account"
#     )
#
#     class Meta:
#         model = Transaction
#         fields = [
#             "id",
#             "debit_account",
#             "debit_account_id",
#             "credit_account",
#             "credit_account_id",
#             "created_at",
#             "description",
#             "amount",
#             "is_voided",
#             "is_reversal",
#             "reversed_transaction",
#         ]
