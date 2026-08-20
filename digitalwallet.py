import time

class DigitalWallet:
    def __init__(self, account_id, pin, daily_limit=5000):
        self.account_id = account_id
        self.pin = pin
        self.balance = 0.0
        self.daily_limit = daily_limit
        self.daily_spent = 0.0
        self.transaction_history = []  # List of tuples (timestamp, type, amount, status)
        self.failed_pin_attempts = 0
        self.is_locked = False

    def verify_balance(self):
        return self.balance

    def _is_fraudulent(self, amount, transaction_type):
        current_time = time.time()
        
        # 1. Multiple failed PIN attempts lock
        if self.is_locked or self.failed_pin_attempts >= 3:
            self.is_locked = True
            return "SUSPICIOUS: Account locked due to multiple failed PIN attempts."

        # 2. More than 5 transactions in 10 minutes
        recent_txs = [tx for tx in self.transaction_history if current_time - tx[0] <= 600 and tx[3] == "SUCCESS"]
        if len(recent_txs) >= 5:
            return "SUSPICIOUS: More than 5 transactions in 10 minutes."

        # 3. Large transaction detection
        if amount > 10000:
            return "SUSPICIOUS: Large transaction limit exceeded."

        # 4. Unusual transaction amount (e.g., negative or fractional anomalies)
        if amount <= 0:
            return "SUSPICIOUS: Unusual or invalid transaction amount."

        # 5. Daily transaction limit check
        if transaction_type in ["withdrawal", "transfer"] and (self.daily_spent + amount > self.daily_limit):
            return "SUSPICIOUS: Daily transaction limit exceeded."

        return None

    def deposit(self, amount):
        fraud_check = self._is_fraudulent(amount, "deposit")
        if fraud_check:
            self.transaction_history.append((time.time(), "deposit", amount, "FLAGGED"))
            return fraud_check
        
        self.balance += amount
        self.transaction_history.append((time.time(), "deposit", amount, "SUCCESS"))
        return "SUCCESS"

    def withdraw(self, amount, input_pin):
        if input_pin != self.pin:
            self.failed_pin_attempts += 1
            fraud_check = self._is_fraudulent(amount, "withdrawal")
            self.transaction_history.append((time.time(), "withdrawal", amount, "FAILED_PIN"))
            return fraud_check if fraud_check else "ERROR: Invalid PIN."

        fraud_check = self._is_fraudulent(amount, "withdrawal")
        if fraud_check:
            self.transaction_history.append((time.time(), "withdrawal", amount, "FLAGGED"))
            return fraud_check

        if amount > self.balance:
            self.transaction_history.append((time.time(), "withdrawal", amount, "INSUFFICIENT_FUNDS"))
            return "ERROR: Insufficient balance."

        self.balance -= amount
        self.daily_spent += amount
        self.failed_pin_attempts = 0
        self.transaction_history.append((time.time(), "withdrawal", amount, "SUCCESS"))
        return "SUCCESS"

    def transfer(self, target_wallet, amount, input_pin):
        if input_pin != self.pin:
            self.failed_pin_attempts += 1
            fraud_check = self._is_fraudulent(amount, "transfer")
            self.transaction_history.append((time.time(), "transfer", amount, "FAILED_PIN"))
            return fraud_check if fraud_check else "ERROR: Invalid PIN."

        # Check duplicate transaction rule (same amount/target within last 5 seconds)
        current_time = time.time()
        for tx in reversed(self.transaction_history):
            if current_time - tx[0] > 5:
                break
            if tx[1] == "transfer" and tx[2] == amount and tx[3] == "SUCCESS":
                self.transaction_history.append((current_time, "transfer", amount, "FLAGGED_DUPLICATE"))
                return "SUSPICIOUS: Duplicate transaction detected."

        fraud_check = self._is_fraudulent(amount, "transfer")
        if fraud_check:
            self.transaction_history.append((current_time, "transfer", amount, "FLAGGED"))
            return fraud_check

        if amount > self.balance:
            self.transaction_history.append((current_time, "transfer", amount, "INSUFFICIENT_FUNDS"))
            return "ERROR: Insufficient balance."

        self.balance -= amount
        self.daily_spent += amount
        self.failed_pin_attempts = 0
        target_wallet.balance += amount
        
        self.transaction_history.append((current_time, "transfer", amount, "SUCCESS"))
        target_wallet.transaction_history.append((current_time, "receive", amount, "SUCCESS"))
        return "SUCCESS"

    def get_history(self):
        return self.transaction_history
