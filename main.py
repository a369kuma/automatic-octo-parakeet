# Implement a class for Accounts that start with $0
# Provide methods to deposit money, withdraw money, and check the current money
# Make sure you can’t take out more money than you have

# Extensions:
# Extend previous definition of Account to have optional interest rate, withdrawal limit, and name

# Create some way of storing multiple accounts and give each account an id. Write a function that takes in two accounts and transfers money from account1 to account2. Write a function that gives you all the money in every account. 

# A Transaction is whenever money is moved in/out of an account. Extend the previous above implementations to keep track of all the Transactions for an Account and create a function that prints them out e.g. “deposit 500 dollars” “withdraw 100 dollars” etc. Write a function that returns all the Transactions of a certain type (deposit/withdraw)

class Accounts:
    def __init__(self):
        # Only store account_id -> balance
        self.accounts = {}

    def deposit_money(self, account_id, amount):
        if amount < 0:
            return "Invalid amount"
        self.accounts.setdefault(account_id, 0)
        self.accounts[account_id] += amount
        return self.accounts[account_id]

    def withdraw_money(self, account_id, amount):
        if amount < 0:
            return "Invalid amount"
        if account_id not in self.accounts:
            return "Account not found"
        if self.accounts[account_id] < amount:
            return "Insufficient funds"
        self.accounts[account_id] -= amount
        return self.accounts[account_id]

    def check_current_money(self, account_id):
        if account_id in self.accounts:
            return self.accounts[account_id]
        return "Account not found"

    def optional_interest_rate(self, account_id, rate):
        if account_id not in self.accounts:
            return "account not found"
        if rate < 0:
            return "Invalid rate"
        self.accounts[account_id] *= (1 + rate)
        return self.accounts[account_id]

    def withdrawal_limit(self, account_id, limit):
        if account_id not in self.accounts:
            return "account not found"
        if limit < 0:
            return "Invalid limit"
        if self.accounts[account_id] > limit:
            return "Withdrawl limit exceeded"
        return self.accounts[account_id]

    def name(self, account_id, name):
        if account_id not in self.accounts:
            return "account not found"
        self.accounts[account_id] = name
        return self.accounts[account_id]

    def multiple_accounts(self, account1_id, account2_id, amount):
        if account1_id not in self.accounts or account2_id not in self.accounts:
            return "account not found"
        if self.accounts[account1_id] < amount:
            return "Insufficient funds"
        self.accounts[account1_id] -= amount
        self.accounts[account2_id] += amount
        return self.accounts[account1_id], self.accounts[account2_id]

    def tracking_transaction(self, account_id, amount):
        if account_id not in self.accounts:
            return "account not found"
        if amount == 0:
            return "no-op"
        if amount < 0:
            if self.accounts[account_id] < -amount:
                return "Insufficient funds"
            self.accounts[account_id] += amount  # amount negative: subtract
            return f"withdraw {-amount} dollars"
        # deposit path
        self.accounts[account_id] += amount
        return f"deposit {amount} dollars"


