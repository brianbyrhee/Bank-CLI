from decimal import Decimal
from datetime import datetime
import pickle

class Bank:
    def __init__(self):
        """Initalize the Bank with no accounts"""
        self.accounts = None

    def createAccount(self, accountID, accountType, deposit):
        """Initialize a CheckingAccount or SavingsAccount, depending on query accountType string"""
        newAccount = CheckingAccount(accountID, accountType, deposit) if accountType == "checking" else SavingsAccount(accountID, accountType, deposit)
        if not self.accounts:
            self.accounts = [newAccount]
        else:
            self.accounts.append(newAccount)

class Account:
    def __init__(self, accountID, accountType, deposit):
        """Initialize attributes of the parent class, with the first deposit as the first transaction"""
        self.accountID = accountID
        self.accountType = accountType.capitalize()
        self.balance = 0
        self.transactions = None
        self.addTransaction(Decimal(deposit), datetime.now(), True)

    def __str__(self):
        """String method for printing Account information"""
        zeroPad = 9 - len(str(self.accountID))
        balanceStr = "{:,.2f}".format(self.balance)
        return self.accountType + "#" + "0" * zeroPad + str(self.accountID) + ",\tbalance: $" + balanceStr

    def printTransactions(self):
        """Print Transactions using object's string method"""
        sortedTransactions = sorted(self.transactions, key= lambda x: x.date)
        for t in sortedTransactions:
            print(t)

    def addTransaction(self, amount, date, trueTransaction):
        """Initialize and add a transaction to the transactions list"""
        newTransaction = Transaction(amount, date, trueTransaction)
        self.balance += amount

        if not self.transactions:
            self.transactions = [newTransaction]
        else:
            self.transactions.append(newTransaction)

class Transaction:
    def __init__(self, amount, date, trueTransaction):
        """Initialize attributes of the transaction object"""
        self.amount = amount
        self.date = date if type(date) == str else date.strftime("%Y") + "-" +  date.strftime("%m") + "-" +  date.strftime("%d")
        self.trueTransaction = trueTransaction

    def __str__(self):
        """String method for printing Transaction information"""
        return self.date + ", $" + "{:,.2f}".format(self.amount)


class CheckingAccount(Account):
    """Child class of derived Account class"""
    def calculateInterest(self):
        """Calculate interest on CheckingAccount object"""
        self.addTransaction(self.balance*Decimal(0.0015), datetime.now(), False)
        if self.balance < 100:
            self.addTransaction(Decimal(-10), datetime.now(), False)


class SavingsAccount(Account):
    """Child class of derived Account class"""
    def isAccountAtTransactionLimit(self, date):
        """Check if we have hit the number of allowed transactions for the SavingsAccount object"""
        year, month, day = date.split("-")
        recentTransactionDates = 0
        recentTransactionMonths = 0
        for t in self.transactions:
            if t.trueTransaction:
                y,m,d = t.date.split("-")
                if d == day:
                    recentTransactionDates += 1
                if m == month:
                    recentTransactionMonths += 1

        return recentTransactionDates >= 2 or recentTransactionMonths >= 5

    def calculateInterest(self):
        """Calculate interest on SavingsAccount object"""
        self.addTransaction(self.balance*Decimal(0.025), datetime.now(), False)

def main():
    accountID = 1
    bank = Bank()
    currAccount = "None"
    while True:
        print("--------------------------------")
        print("Currently selected account: " + str(currAccount))
        print("Enter command")
        print("1: open account")
        print("2: summary")
        print("3: select account")
        print("4: list transactions")
        print("5: add transaction")
        print("6: interest and fees")
        print("7: save")
        print("8: load")
        print("9: quit")
        task = input(">")

        if task == "1":
            # 1: open account
            print("Type of account? (checking/savings)")
            accountType = input(">")
            print("Initial deposit amount?")
            deposit = input(">")
            bank.createAccount(accountID, accountType, deposit)
            accountID += 1
        
        elif task == "2":
            # 2: summary
            for acc in bank.accounts:
                print(acc)
        
        elif task == "3":
            # 3: select account
            print("Enter account number")
            accNumber = input(">")
            currAccount = bank.accounts[int(accNumber)-1]

        elif task == "4":
            # 4: list transactions
            currAccount.printTransactions()

        elif task == "5":
            # 5: add transaction
            print("Amount?")
            amount = input(">")
            print("Date? (YYYY-MM-DD)")
            date = input(">")

            # check if we're exceeding the trans limit
            if currAccount.balance + Decimal(amount) < 0:
                continue
            if type(currAccount) is SavingsAccount and currAccount.isAccountAtTransactionLimit(date):
                continue
                
            currAccount.addTransaction(Decimal(amount), date, True)

        elif task == "6":
            # 6: interest and fees
            if type(currAccount) is SavingsAccount:
                currAccount.calculateInterest()
            elif type(currAccount) is CheckingAccount:
                currAccount.calculateInterest()

        elif task == "7":
            # 7: save
            pickle.dump(bank, open("save.p", "wb"))

        elif task == "8":
            # 8: load
            bank = pickle.load(open("save.p", "rb"))

        elif task == "9":
            # 9: quit
            return
        
        else:
            pass



if __name__ == "__main__":
    main()
