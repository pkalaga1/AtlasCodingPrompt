from transactions import Transaction
from user_activity import UserActivity
from datetime import datetime, timedelta
import csv

class FraudDetection():

    FIELDS = ['user ID', 'timestamp', 'merchant name', 'amount']
    DATETIME_FORMAT = '%m-%d-%Y %H:%M:%S'

    amount_diff_threshold: float
    large_time_diff_threshold: timedelta
    num_transaction_threshold_for_avg: int
    too_many_refunds_percentage_threshold: float
    num_transaction_threshold_for_refunds: int
    num_transaction_threshold_for_frequent_transactions: int
    small_time_diff_threshold: timedelta
    

    def __init__(
            self, 
            amount_diff_threshold: float = 100.00,
            large_time_diff_threshold: timedelta = timedelta(days=1),
            num_transaction_threshold_for_avg: int = 5,
            too_many_refunds_percentage_threshold: float = .45,
            num_transaction_threshold_for_refunds: int = 5,
            small_time_diff_threshold: timedelta = timedelta(seconds=1),
            num_transaction_threshold_for_frequent_transactions: int = 5,
    ) -> None:
        self.amount_diff_threshold = amount_diff_threshold
        self.large_time_diff_threshold = large_time_diff_threshold
        self.num_transaction_threshold_for_avg = num_transaction_threshold_for_avg
        self.too_many_refunds_percentage_threshold=too_many_refunds_percentage_threshold
        self.num_transaction_threshold_for_refunds=num_transaction_threshold_for_refunds
        self.small_time_diff_threshold = small_time_diff_threshold
        self.num_transaction_threshold_for_frequent_transactions = num_transaction_threshold_for_frequent_transactions
        self.users = {}

    def detect_fraud(self, file_path):
        flagged_transactions = []
        with open(file_path, newline='') as csv_file:
            all_transactions = csv.DictReader(csv_file, delimiter=',')

            for transaction in all_transactions:
                uid = transaction['user ID']
                transaction_time = datetime.strptime(transaction['timestamp'], self.DATETIME_FORMAT)
                merchant_name = transaction["merchant name"]
                amount = float(transaction['amount'])

                if uid not in self.users:
                    self.users[uid] = UserActivity(uid)
                
                user_activity: UserActivity = self.users[uid]
                usr_transaction: Transaction = Transaction(amount=amount, transaction_time=transaction_time, merchant_name=merchant_name)

                flag = False
                flag = flag or user_activity.greater_than_average(
                    amount=amount, 
                    diff_threshold=self.amount_diff_threshold, 
                    num_transactions_threshold=self.num_transaction_threshold_for_avg
                    )
                    
                flag = flag or user_activity.is_large_transaction_time_difference(
                        transaction_time=transaction_time, 
                        diff_threshold=self.large_time_diff_threshold, 
                    )

                flag = flag or user_activity.add_transaction_with_flags(transaction=usr_transaction)

                flag = flag or user_activity.check_too_many_refunds(
                        percent_threshold=self.too_many_refunds_percentage_threshold,
                        num_transactions_threshold=self.num_transaction_threshold_for_refunds
                    )
                
                flag = flag or user_activity.check_high_frequency_transactions(
                    num_transactions_threshold=self.num_transaction_threshold_for_frequent_transactions,
                    time_threshold=self.small_time_diff_threshold
                )
                
                if flag:
                    flagged_transactions.append(transaction)


        
        with open('flagged_transactions.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.FIELDS)
            writer.writeheader()
            writer.writerows(flagged_transactions)