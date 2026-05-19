from enum import Enum

class PaymentType(str,Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"
    CASH = "cash"

class PaymentStatus(str,Enum):
    PENDING = "pending"
    COMPLETE = "completer"
    FAIL = "fail"