import pytest
from django.core.management import call_command

from accounting.models import Account, BalanceGroup, Transaction


@pytest.fixture(autouse=True)
def load_fixtures(db):
    call_command("loaddata", "accounting/fixtures/test_data.json")


@pytest.mark.django_db
def test_active_to_active():
    group = BalanceGroup.objects.get(pk=1)
    debit = Account.objects.create(
        name="Актив Дебет", type="active", balance=5000, balance_group=group
    )
    credit = Account.objects.create(
        name="Актив Кредит", type="active", balance=3000, balance_group=group
    )

    txn = Transaction(debit_account=debit, credit_account=credit, amount=1000)
    txn.update_balance()

    debit.refresh_from_db()
    credit.refresh_from_db()

    assert debit.balance == 6000  # Debit increased
    assert credit.balance == 2000  # Credit decreased


@pytest.mark.django_db
def test_passive_to_passive():
    group = BalanceGroup.objects.get(pk=2)
    debit = Account.objects.create(
        name="Пассив Дебет", type="passive", balance=4000, balance_group=group
    )
    credit = Account.objects.create(
        name="Пассив Кредит", type="passive", balance=2500, balance_group=group
    )

    txn = Transaction(debit_account=debit, credit_account=credit, amount=500)
    txn.update_balance()

    debit.refresh_from_db()
    credit.refresh_from_db()

    assert debit.balance == 3500  # Debit decreased
    assert credit.balance == 3000  # Credit decreased


@pytest.mark.django_db
def test_active_to_passive():
    debit_group = BalanceGroup.objects.get(pk=1)
    credit_group = BalanceGroup.objects.get(pk=2)

    debit = Account.objects.create(
        name="Актив Дебет", type="active", balance=7000, balance_group=debit_group
    )
    credit = Account.objects.create(
        name="Пассив Кредит", type="passive", balance=2000, balance_group=credit_group
    )

    txn = Transaction(debit_account=debit, credit_account=credit, amount=1000)
    txn.update_balance()

    debit.refresh_from_db()
    credit.refresh_from_db()

    assert debit.balance == 8000  # Debit increased
    assert credit.balance == 3000  # Credit increased


@pytest.mark.django_db
def test_passive_to_active():
    debit_group = BalanceGroup.objects.get(pk=2)
    credit_group = BalanceGroup.objects.get(pk=1)

    debit = Account.objects.create(
        name="Пассив Дебет", type="passive", balance=5000, balance_group=debit_group
    )
    credit = Account.objects.create(
        name="Актив Кредит", type="active", balance=6000, balance_group=credit_group
    )

    txn = Transaction(debit_account=debit, credit_account=credit, amount=1500)
    txn.update_balance()

    debit.refresh_from_db()
    credit.refresh_from_db()

    assert debit.balance == 3500  # Debit decreased
    assert credit.balance == 4500  # Credit decreased
