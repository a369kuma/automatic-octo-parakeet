import unittest
from main import Accounts

class TestAccounts(unittest.TestCase):
    def setUp(self):
        self.accounts = Accounts()

    def test_deposit_to_new_account(self):
        account_id = "acc1"
        self.accounts.deposit_money(account_id, 500)
        self.assertEqual(self.accounts.check_current_money(account_id), 500)

    def test_deposit_to_existing_account(self):
        account_id = "acc1"
        self.accounts.deposit_money(account_id, 500)
        self.accounts.deposit_money(account_id, 300)
        self.assertEqual(self.accounts.check_current_money(account_id), 800)

    def test_withdraw_with_sufficient_funds(self):
        account_id = "acc1"
        self.accounts.deposit_money(account_id, 500)
        self.accounts.withdraw_money(account_id, 200)
        self.assertEqual(self.accounts.check_current_money(account_id), 300)

    def test_withdraw_with_insufficient_funds(self):
        account_id = "acc1"
        self.accounts.deposit_money(account_id, 100)
        result = self.accounts.withdraw_money(account_id, 200)
        self.assertEqual(result, "Insufficient funds")
        self.assertEqual(self.accounts.check_current_money(account_id), 100)

    def test_check_balance_for_nonexistent_account(self):
        account_id = "nonexistent"
        result = self.accounts.check_current_money(account_id)
        self.assertEqual(result, "Account not found")

    def test_interest_rate_applied(self):
        account_id = "acc_int"
        self.accounts.deposit_money(account_id, 1000)
        new_balance = self.accounts.optional_interest_rate(account_id, 0.10)
        self.assertAlmostEqual(new_balance, 1100)

    def test_interest_invalid_rate(self):
        account_id = "acc_int_bad"
        self.accounts.deposit_money(account_id, 500)
        result = self.accounts.optional_interest_rate(account_id, -0.05)
        self.assertEqual(result, "Invalid rate")

    def test_withdrawal_limit_exceeded(self):
        account_id = "acc_lim1"
        self.accounts.deposit_money(account_id, 600)
        result = self.accounts.withdrawal_limit(account_id, 500)
        self.assertEqual(result, "Withdrawl limit exceeded")

    def test_withdrawal_limit_not_exceeded(self):
        account_id = "acc_lim2"
        self.accounts.deposit_money(account_id, 400)
        result = self.accounts.withdrawal_limit(account_id, 500)
        self.assertEqual(result, 400)

    def test_withdrawal_limit_invalid_limit(self):
        account_id = "acc_lim3"
        self.accounts.deposit_money(account_id, 100)
        result = self.accounts.withdrawal_limit(account_id, -1)
        self.assertEqual(result, "Invalid limit")

    def test_name_replaces_balance_with_string(self):
        account_id = "acc_name"
        self.accounts.deposit_money(account_id, 250)
        named = self.accounts.name(account_id, "Primary Account")
        self.assertEqual(named, "Primary Account")
        self.assertEqual(self.accounts.check_current_money(account_id), "Primary Account")

    # New tests for transfer functionality
    def test_transfer_success(self):
        a1, a2 = "t1", "t2"
        self.accounts.deposit_money(a1, 500)
        self.accounts.deposit_money(a2, 200)
        new_bal_a1, new_bal_a2 = self.accounts.multiple_accounts(a1, a2, 150)
        self.assertEqual(new_bal_a1, 350)
        self.assertEqual(new_bal_a2, 350)

    def test_transfer_insufficient_funds(self):
        a1, a2 = "t3", "t4"
        self.accounts.deposit_money(a1, 50)
        self.accounts.deposit_money(a2, 10)
        result = self.accounts.multiple_accounts(a1, a2, 200)
        self.assertEqual(result, "Insufficient funds")
        self.assertEqual(self.accounts.check_current_money(a1), 50)
        self.assertEqual(self.accounts.check_current_money(a2), 10)

    def test_transfer_missing_account(self):
        a1, a2 = "t5", "missing"
        self.accounts.deposit_money(a1, 100)
        result = self.accounts.multiple_accounts(a1, a2, 20)
        self.assertEqual(result, "account not found")

    # New tests for tracking_transaction
    def test_tracking_transaction_deposit(self):
        acc = "tr1"
        self.accounts.deposit_money(acc, 100)
        msg = self.accounts.tracking_transaction(acc, 40)
        self.assertEqual(msg, "deposit 40 dollars")
        self.assertEqual(self.accounts.check_current_money(acc), 140)

    def test_tracking_transaction_withdraw(self):
        acc = "tr2"
        self.accounts.deposit_money(acc, 200)
        msg = self.accounts.tracking_transaction(acc, -60)
        self.assertEqual(msg, "withdraw 60 dollars")
        self.assertEqual(self.accounts.check_current_money(acc), 140)

    def test_tracking_transaction_withdraw_insufficient(self):
        acc = "tr3"
        self.accounts.deposit_money(acc, 30)
        msg = self.accounts.tracking_transaction(acc, -50)
        self.assertEqual(msg, "Insufficient funds")
        self.assertEqual(self.accounts.check_current_money(acc), 30)

    def test_tracking_transaction_missing_account(self):
        msg = self.accounts.tracking_transaction("ghost", 10)
        self.assertEqual(msg, "account not found")

    def test_tracking_transaction_no_op(self):
        acc = "tr4"
        self.accounts.deposit_money(acc, 10)
        msg = self.accounts.tracking_transaction(acc, 0)
        self.assertEqual(msg, "no-op")
        self.assertEqual(self.accounts.check_current_money(acc), 10)

if __name__ == "__main__":
    unittest.main()
