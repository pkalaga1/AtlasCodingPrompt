from transactions import Transaction
from datetime import datetime, timedelta
class UserActivity:

    id: int
    transactions: list[Transaction]
    average: float
    num_refunds: int
    merchants: dict


    def __init__(self, id: int) -> None:
        self.id = id
        self.transactions = []
        self.average = 0.0
        self.num_refunds = 0
        self.merchants = {}

    def add_transaction_with_flags(self, transaction: Transaction):
        flag = False
        self.transactions.append(transaction)
        self.average = (self.average + transaction.amount) / len(self.transactions)

        if transaction.amount < 0:
            self.num_refunds += 1
            flag = self.flag_refunds(transaction)
        else:
            if transaction.merchant_name not in self.merchants:
                self.merchants[transaction.merchant_name] = []
            self.merchants[transaction.merchant_name].append(transaction.amount)
        
        return flag

    def greater_than_average(self, amount: float, diff_threshold: float, num_transactions_threshold: int):
        if len(self.transactions) < num_transactions_threshold:
            return False
        
        if amount - self.average >= diff_threshold:
            return True
        return False
    
    def is_large_transaction_time_difference(self, transaction_time: datetime, diff_threshold: timedelta):
        if len(self.transactions) == 0:
            return False
        
        last_transaction_time: datetime = self.transactions[-1].transaction_time
        if transaction_time - last_transaction_time > diff_threshold:
            return True
        return False

    def flag_refunds(self, transaction: Transaction):
        if self.num_refunds >= len(self.transactions):
            return True
        
        if transaction.merchant_name not in self.merchants:
            return True
        else:
            # This is naive, but we dont have a way to link transactions and refunds
            # so we are just gonna check if there is an amount larger or equal to
            # the refund amount
            for amount in self.merchants[transaction.merchant_name]:
                if abs(transaction.amount) > amount:
                    return True


        return False
    
    def check_too_many_refunds(self, percent_threshold: float, num_transactions_threshold: int):
        if (
            len(self.transactions) >= num_transactions_threshold 
            and float(self.num_refunds) / len(self.transactions) > percent_threshold
        ):
            return True
        
        return False
    
    # This assumes that the threshold is at least 2
    def check_high_frequency_transactions(self, num_transactions_threshold: int, time_threshold: timedelta):
        if len(self.transactions) > num_transactions_threshold:
            start = len(self.transactions) - num_transactions_threshold
            flag = True
            
            sub_arr = self.transactions[start:]
            for i in range(1, len(sub_arr)):
                if sub_arr[i].transaction_time - sub_arr[i-1].transaction_time > time_threshold:
                    flag = False
                    break
                
            if flag:
                return True

        return False


