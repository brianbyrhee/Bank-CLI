from decimal import Decimal
from datetime import datetime
import pickle

class Bank:
    def __init__(self):
        self.accounts = None

    def createAccount(self, accountID, accountType, deposit):
        newAccount = CheckingAccount(accountID, accountType, deposit) if accountType == "checking" else SavingsAccount(accountID, accountType, deposit)
        if not self.accounts:
            self.accounts = [newAccount]
        else:
            self.accounts.append(newAccount)

class Account:
    def __init__(self, accountID, accountType, deposit):
        self.accountID = accountID
        self.accountType = accountType.capitalize()
        self.deposit = 0
        self.transactions = None
        self.trueTransactionCounter = 0
        self.addTransaction(Decimal(deposit), datetime.now(), True)

    def printTransactions(self):
        sortedTransactions = sorted(self.transactions, key= lambda x: x.date)
        for t in sortedTransactions:
            print(t.date + ", $" + "{:,.2f}".format(t.amount))

    def addTransaction(self, amount, date, trueTransaction):
        newTransaction = Transaction(amount, date, trueTransaction)
        self.deposit += amount

        if not self.transactions:
            self.transactions = [newTransaction]
        else:
            self.transactions.append(newTransaction)

class Transaction:
    def __init__(self, amount, date, trueTransaction):
        self.amount = amount
        self.date = date if type(date) == str else date.strftime("%Y") + "-" +  date.strftime("%m") + "-" +  date.strftime("%d")
        self.trueTransaction = trueTransaction

class CheckingAccount(Account):
    def calculateInterest(self):
        pass


class SavingsAccount(Account):
    def checkTransactionCountLimit(self):
        pass

    def calculateInterest(self):
        pass

def parseInfo(acc):
    zeroPad = 9 - len(str(acc.accountID))
    #depositStr = "%.2f" % acc.deposit
    depositStr = "{:,.2f}".format(acc.deposit)
    return acc.accountType + "#" + "0" * zeroPad + str(acc.accountID) + ",\tbalance: $" + depositStr

def main():
    accountID = 1
    bank = Bank()
    currAccount = "None"
    while True:
        # doublecheck on what exactly needs to be printed below
        accountPrint = currAccount if currAccount == "None" else parseInfo(currAccount)
        print("--------------------------------")
        print("Currently selected account: " + accountPrint)
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
            year, month, day = date.split("-")

            # check if we're exceeding the trans limit
            if currAccount.deposit + Decimal(amount) < 0:
                continue
            if type(currAccount) is SavingsAccount:
                recentTransactionDates = []
                for i in range(len(currAccount.transactions)-1,-1,-1):
                    if currAccount.transactions[i].trueTransaction:
                        recentTransactionDates.append(currAccount.transactions[i].date.split("-"))
                    if len(recentTransactionDates) == 2:
                        break

                recentTransactionMonths = []
                for i in range(len(currAccount.transactions)-1,-1,-1):
                    if currAccount.transactions[i].trueTransaction:
                        recentTransactionMonths.append(currAccount.transactions[i].date.split("-"))
                    if len(recentTransactionMonths) == 5:
                        break

                if (len(recentTransactionDates) == 2 and all(d == day for _,_,d in recentTransactionDates)) or (len(recentTransactionMonths) == 5 and all(m == month for _,m,_ in recentTransactionMonths)):
                    continue
            
                
            currAccount.addTransaction(Decimal(amount), date, True)

        elif task == "6":
            # 6: interest and fees
            if type(currAccount) is SavingsAccount:
                currAccount.addTransaction(currAccount.deposit*Decimal(0.025), datetime.now(), False)
            elif type(currAccount) is CheckingAccount:
                currAccount.addTransaction(currAccount.deposit*Decimal(0.0015), datetime.now(), False)
                if currAccount.deposit < 100:
                    currAccount.addTransaction(Decimal(-10), datetime.now(), False)

        elif task == "7":
            # 7: save
            pickle.dump(bank, open("save.p", "wb"))

        elif task == "8":
            # 8: load
            pickle.load(open("save.p", "rb"))

        elif task == "9":
            # 9: quit
            return
        
        else:
            pass



if __name__ == "__main__":
    main()
