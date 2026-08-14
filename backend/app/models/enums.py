from enum import Enum


class AccountType(str, Enum):
    CASH = "CASH"
    BANK = "BANK"
    WALLET = "WALLET"
    CREDIT_CARD = "CREDIT_CARD"
    OTHER = "OTHER"


class AccountNature(str, Enum):
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"


class TransactionType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    TRANSFER = "TRANSFER"
    REFUND = "REFUND"


class TransactionSource(str, Enum):
    MANUAL = "MANUAL"
    IMPORT = "IMPORT"


class CategoryType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    BOTH = "BOTH"