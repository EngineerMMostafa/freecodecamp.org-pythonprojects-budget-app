class Category:
    # Define Category Calss

    def __init__ (self, name):    
        # Initiate needed attributes in constructor
        # name of the category    
        self.name = name
        # Empty ledger list
        self.ledger = list()
        # sum of total withdraw actions
        self.total_withdraw = 0

    def get_balance(self):
        # Function to calculate self category balance
        avl_amount = 0
        for item in self.ledger:
            avl_amount += item["amount"]
        return(avl_amount)

    def check_funds(self, amount):
        # Function to check required amount VS available balance
        if amount > self.get_balance():
            return False
        else:
            return True
        
    def deposit(self, amount, description = ''):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description = ''):
        if self.check_funds(amount):
            self.deposit((amount * -1), description)
            # add withdraw amount to total_withdraw attribute
            self.total_withdraw += amount
            return True
        else:
            return False

    def transfer(self, amount, otherbudget):
        if self.check_funds(amount):
            self.deposit((amount * -1), ('Transfer to %s'%otherbudget.name))
            otherbudget.deposit(amount, 'Transfer from %s'%self.name)
            return True
        else:
            return False

    def __repr__(self):
        # Function __repr__ to define the Instance representation
        txt = self.name.center(30, '*') + '\n'
        for i in self.ledger:
            if len(i["description"]) > 23:
                txt += i["description"][:(29-len("{:.2f}".format(i["amount"])))] + ' ' + "{:.2f}".format(i["amount"]) + '\n'
            else:
                txt += i["description"].ljust(23) + "{:.2f}".format(i["amount"]).rjust(7) + '\n'
        txt += 'Total: ' + str(self.get_balance())

        return txt
    
def create_spend_chart(categories):
    # takes a list of categories as an argument and return a string that is a bar chart of withdraws.
    p = 100                   # vl-scale
    n = len(categories)       # number of input categories
    total_withdraws = 0

    # Sum input categories waithdraws in total_withdraws
    for c in categories:
        total_withdraws += c.total_withdraw

    # construct bar chart string
    chart = "Percentage spent by category" + '\n'
    while p >= 0:
        # add chart scale right
        chart += str(p).rjust(3) + '| '
        for c in categories:
            # For each category, calculate withdraw Percentage
            perc = c.total_withdraw * 100 / total_withdraws
            perc = (int(perc/10))*10      # round down to nearest 10
            if perc >= p:
                chart += 'o'.ljust(3)
            else:
                chart += ''.ljust(3)
        chart += '\n'
        # decrement scale
        p -= 10
    # Add chart separator line '------------'
    chart += ''.rjust(4) + ''.rjust(1+3*n,'-') + '\n'

    # Add categories names vertically
    names = list()
    for c in categories:
        names.append(len(c.name))
    
    for i in range(max(names)):
        chart += ''.rjust(5)
        for c in categories:
            if len(c.name) > i:
                chart += c.name[i] + '  '
            else:
                chart += '   '
        if i != max(names)-1:
            chart += '\n'

    return chart
