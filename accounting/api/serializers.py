from rest_framework import serializers

from accounting.models import (
    Transaction,
    Account,
    BalanceGroup,
    BalanceSheetItem,
)


class BalanceSheetItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceSheetItem
        fields = ["id", "name"]


class BalanceGroupSerializer(serializers.ModelSerializer):
    balance_sheet_item = BalanceSheetItemSerializer(read_only=True)
    balance_sheet_item_id = serializers.PrimaryKeyRelatedField(
        queryset=BalanceSheetItem.objects.all(),
        write_only=True,
        source="balance_sheet_item",
    )

    class Meta:
        model = BalanceGroup
        fields = ["id", "name", "balance_sheet_item", "balance_sheet_item_id"]


class AccountSerializer(serializers.ModelSerializer):
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


class TransactionSerializer(serializers.ModelSerializer):
    debit_account = AccountSerializer(read_only=True)
    debit_account_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(), write_only=True, source="debit_account"
    )
    credit_account = AccountSerializer(read_only=True)
    credit_account_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(), write_only=True, source="credit_account"
    )

    class Meta:
        model = Transaction
        fields = [
            "id",
            "debit_account",
            "debit_account_id",
            "credit_account",
            "credit_account_id",
            "created_at",
            "description",
            "amount",
            "is_voided",
            "reversed_transaction",
        ]
