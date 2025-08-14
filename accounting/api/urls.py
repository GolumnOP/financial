from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AccountView,
    BalanceSheetItemView,
    BalanceGroupView,
    # TransactionView,
    AccountsListView,
)

router = DefaultRouter()
router.register(r"accounts", AccountView)
router.register(r"balance-sheet-items", BalanceSheetItemView)
router.register(r"balance-group", BalanceGroupView)
# router.register(r"transactions", TransactionView)

urlpatterns = [
    path("", include(router.urls)),
    path("accounts-list/", AccountsListView.as_view(), name="account_list"),

]
