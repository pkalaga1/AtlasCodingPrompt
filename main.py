from fraud_detection import FraudDetection
from datetime import timedelta

def main():

    amount_diff_threshold: float = 100.00
    large_time_diff_threshold: timedelta = timedelta(days=1)
    num_transaction_threshold_for_avg: int = 5
    too_many_refunds_percentage_threshold: float = .45
    num_transaction_threshold_for_refunds: int = 5
    num_transaction_threshold_for_frequent_transactions: int = 5
    small_time_diff_threshold: timedelta = timedelta(seconds=1)

    detection_tool = FraudDetection(
        amount_diff_threshold=amount_diff_threshold,
        large_time_diff_threshold=large_time_diff_threshold,
        num_transaction_threshold_for_avg=num_transaction_threshold_for_avg,
        too_many_refunds_percentage_threshold=too_many_refunds_percentage_threshold,
        num_transaction_threshold_for_frequent_transactions=num_transaction_threshold_for_frequent_transactions,
        num_transaction_threshold_for_refunds=num_transaction_threshold_for_refunds,
        small_time_diff_threshold=small_time_diff_threshold
    )

    file_path = 'transactions.csv'

    detection_tool.detect_fraud(file_path=file_path)




if __name__ == "__main__":
    main()