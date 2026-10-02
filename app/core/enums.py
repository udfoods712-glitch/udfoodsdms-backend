from enum import Enum


class UserRole(str, Enum):
    OWNER = "OWNER"
    DRIVER = "DRIVER"

class DeliveryStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    IN_TRANSIT = "IN_TRANSIT"
    COMPLETED = "COMPLETED"

class PaymentLocation(str, Enum):
    BANK_SBI = "BANK_SBI"
    BANK_JNK = "BANK_JNK"
    SHOP_ZIRAKPUR = "SHOP_ZIRAKPUR"
    CASH = "CASH"