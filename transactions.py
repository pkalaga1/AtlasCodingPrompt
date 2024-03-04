from datetime import datetime
from dataclasses import dataclass

@dataclass
class Transaction:

    amount: float
    transaction_time: datetime
    merchant_name: str
