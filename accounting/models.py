from django.db import models, transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from financial.utils import create_acc_number


class BalanceSheetItem(models.Model):
    """
    Статья бухгалтерского баланса
    """

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BalanceGroup(models.Model):
    """
    Балансовая группа, относится к статье бухгалтерского баланса
    """

    name = models.CharField(max_length=255)
    balance_sheet = models.ForeignKey(
        BalanceSheetItem, on_delete=models.CASCADE, related_name="groups"
    )

    def __str__(self):
        return f"Balance group: {self.name}"


class Account(models.Model):
    """
    Cчёт, относится к балансовой группе
    """

    ACCOUNT_TYPE = [
        ("active", "Active"),
        ("passive", "Passive"),
        ("active-passive", "Active-passive"),
    ]

    number = models.CharField(
        max_length=10, editable=False, unique=True, default=create_acc_number
    )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=15, choices=ACCOUNT_TYPE)
    balance_group = models.ForeignKey(
        BalanceGroup, on_delete=models.CASCADE, related_name="accounts"
    )
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    def __str__(self):
        return f"Account number | name: {self.number} | {self.name}"


#
class Transaction(models.Model):
    """
    Учёт транзакции с возможностью ее отмены
    """

    debit_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="debit_transactions"
    )
    credit_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="credit_transactions"
    )
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=600, blank=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2)

    # Отмена транзакции
    is_voided = models.BooleanField(default=False)
    reversed_transaction = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="original_transactions",
    )

    class Meta:
        ordering = ["-created_at"]

    def valid_transaction(self):
        """
        1) 'Оба счёта должны быть выбраны'
        2) 'Создается 1 поле amount -> Сумма по дебету = сумма по кредиту'
        """
        if not self.credit_account or not self.debit_account:
            raise ValidationError("Both credit and debit must be selected")
        if self.credit_account == self.debit_account:
            raise ValidationError("Credit and debit can't be the same account")
        if self.amount is None or self.amount <= 0:
            raise ValidationError("Sum must be positive")

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.valid_transaction()
            with transaction.atomic():
                self.update_balance()
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def update_balance(self):
        """
        '3) Поддержка логики двойной записи (см. ниже)
        Актив → Актив	Один актив уменьшается (кредит), другой увеличивается (дебет)
        Пассив → Пассив	Один пассив уменьшается (дебет), другой увеличивается (кредит)
        Актив → Пассив	Актив увеличивается (дебет), пассив увеличивается (кредит)
        Пассив → Актив	Пассив уменьшается (дебет), актив уменьшается (кредит)'
        """

        credit_type = self.credit_account.type
        debit_type = self.debit_account.type

        # TODO: how to count active-passive types?

        if debit_type == "active" and credit_type == "active":
            self.debit_account.balance += self.amount
            self.credit_account.balance -= self.amount
        elif debit_type == "passive" and credit_type == "passive":
            self.debit_account.balance -= self.amount
            self.credit_account.balance += self.amount
        elif debit_type == "active" and credit_type == "passive":
            self.debit_account.balance += self.amount
            self.credit_account.balance += self.amount
        elif debit_type == "passive" and credit_type == "active":
            self.debit_account.balance -= self.amount
            self.credit_account.balance -= self.amount
        else:
            raise ValidationError("Invalid acc type combination")

        self.credit_account.save()
        self.debit_account.save()

    # TODO: add voided transaction logic

    def __str__(self):
        return f"debit: {self.debit_account} | credit: {self.credit_account}"
