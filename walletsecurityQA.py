import time
import threading
from digitalwallet import DigitalWallet

def run_test_suite():
    print("--- STARTING QA SECURITY TEST SUITE ---\n")

    # 1. Test: Normal transaction
    w1 = DigitalWallet("ACC01", 1234)
    w2 = DigitalWallet("ACC02", 5678)
    assert w1.deposit(1000) == "SUCCESS", "Normal deposit failed"
    assert w1.transfer(w2, 200, 1234) == "SUCCESS", "Normal transfer failed"
    assert w1.verify_balance() == 800, "Balance mismatch after normal transaction"
    print("Test Normal transaction: PASSED")

    # 2. Test: Insufficient balance
    res = w1.withdraw(5000, 1234)
    assert "Insufficient balance" in res, "Failed to trap insufficient funds"
    print("Test Insufficient balance: PASSED")

    # 3. Test: Daily limit
    w_limit = DigitalWallet("ACC_LIMIT", 1234, daily_limit=500)
    w_limit.deposit(1000)
    w_limit.withdraw(400, 1234)
    res = w_limit.withdraw(200, 1234)
    assert "Daily transaction limit exceeded" in res, "Failed to restrict daily cap"
    print("Test Daily limit: PASSED")

    # 4. Test: Multiple failed PINs
    w_pin = DigitalWallet("ACC_PIN", 1234)
    w_pin.deposit(500)
    w_pin.withdraw(100, 9999)
    w_pin.withdraw(100, 9999)
    res = w_pin.withdraw(100, 9999)
    assert "multiple failed PIN attempts" in res, "Failed to activate PIN failure lock"
    print("Test Multiple failed PINs: PASSED")

    # 5. Test: Suspicious transaction (High frequency & large amounts)
    w_sus = DigitalWallet("ACC_SUS", 1234)
    w_sus.deposit(20000)
    # Frequency: 5 rapid successful deposits, the 6th must trigger rate alert
    for _ in range(5):
        w_sus.deposit(10)
    res = w_sus.deposit(10)
    assert "More than 5 transactions in 10 minutes" in res, "Frequency trap failed"
    
    res_large = w_sus.deposit(50000)
    assert "Large transaction limit exceeded" in res_large, "High value trigger failed"
    print("Test Suspicious transaction: PASSED")

    # 6. Test: Duplicate transaction
    w_dup1 = DigitalWallet("ACC_DUP1", 1234)
    w_dup2 = DigitalWallet("ACC_DUP2", 5678)
    w_dup1.deposit(1000)
    w_dup1.transfer(w_dup2, 100, 1234)
    res = w_dup1.transfer(w_dup2, 100, 1234)
    assert "Duplicate transaction detected" in res, "Rapid replication trap failed"
    print("Test Duplicate transaction: PASSED")

    # 7. Test: Negative amount
    w_neg = DigitalWallet("ACC_NEG", 1234)
    res = w_neg.deposit(-50)
    assert "Unusual or invalid transaction amount" in res, "Negative entry trap failed"
    print("Test Negative amount: PASSED")

    # 8. Test: Concurrent transactions
    w_conc = DigitalWallet("ACC_CONC", 1234)
    w_conc.deposit(100)
    
    def target_task():
        w_conc.withdraw(10, 1234)

    threads = [threading.Thread(target=target_task) for _ in range(3)]
    for t in threads: t.start()
    for t in threads: t.join()
    # Verifies state mutation history logs multiple interactions simultaneously 
    assert len(w_conc.get_history()) >= 4, "Concurrency trace missing steps"
    print("Test Concurrent transactions: PASSED")

    print("\n--- ALL QA SECURITY SUITE TESTS COMPLETED SUCCESSFULLY ---")

if __name__ == "__main__":
    run_test_suite()
