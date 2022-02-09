import decimal
import math

class Bank:
    def __init__(self):
        self.accounts = None

    def createAccount(self, accountID, accountType, deposit):
        newAccount = Account(accountID, accountType, deposit)
        if not self.accounts:
            self.accounts = [newAccount]
        else:
            self.accounts.append(newAccount)

class Account:
    def __init__(self, accountID, accountType, deposit):
        self.accountID = accountID
        self.accountType = accountType
        # deposit is a string
        decimal.getcontext().prec = 2
        decimal.getcontext().rounding = decimal.ROUND_HALF_UP
        self.deposit = decimal.Decimal(deposit)
        self.transactions = None

    def printTransactions(self):
        for t in self.transactions:
            print(t.date + ", " + t.amount)

    def addTransaction(self, amount, date):
        newTransaction = Transaction(amount, date)
        self.deposit += amount
        if not self.transactions:
            self.transactions = [newTransaction]
        else:
            self.transactions.append(newTransaction)

class Transaction:
    def __init__(self, amount, date):
        self.amount = amount
        self.date = date

class CheckingAccount(Account):
    def __init__(self):
        pass

class SavingsAccount(Account):
    def __init__(self):
        pass

def parseInfo(acc):
    zeroPad = 9 - acc.accountID
    #depositStr = "%.2f" % acc.deposit
    depositStr = str(acc.deposit)
    return acc.accountType + "#" + "0" * zeroPad + str(acc.accountID) + ",\tbalance: " + depositStr

def main():
    accountID = 1
    bank = Bank()
    while True:
        currAccount = "None"
        # doublecheck on what exactly needs to be printed below
        print("Currently selected account: " + currAccount)
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
                # clean this up and test for the deposit value
                accInfo = parseInfo(acc)
                print(accInfo)
        
        elif task == "3":
            # 3: select account
            print("Enter account number")
            print(len(bank.accounts))
            accNumber = input(">")
            currAccount = parseInfo(bank.accounts[int(accNumber)-1])
            

        elif task == "4":
            # 4: list transactions
            currAccount.printTransactions()

        elif task == "5":
            # 5: add transaction
            print("Amount?")
            amount = input(">")
            print("Date? (YYYY-MM-DD)")
            date = input(">")
            year, month, day = date.split("-")

            # check if we're exceeding the trans limit
            if currAccount.deposit + amount < 0:
                continue
            if type(currAccount) is SavingsAccount:
                recentTransactionDates = [c.split("-") for c in currAccount.transactions[-2:]]
                recentTransactionMonths = [c.split("-") for c in currAccount.transactions[-5:]]
                if all(d == day for _,_,d in recentTransactionDates) or all(m == month for _,m,_ in recentTransactionMonths):
                    continue
            
            currAccount.addTransaction(amount, date)

        elif task == "6":
            # 6: interest and fees
            pass

        elif task == "7":
            # 7: save
            pass

        elif task == "8":
            # 8: load
            pass

        elif task == "9":
            # 9: quit
            return
        
        else:
            pass



if __name__ == "__main__":
    main()
