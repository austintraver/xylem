import json

class Result:
    def __init__(self, ticker, buys, sells, orders, starting_balance, ending_balance):
        self.ticker = ticker
        self.buys = buys
        self.sells = sells
        self.orders = orders
        self.starting_balance = starting_balance
        self.ending_balance = ending_balance

    def json(self):
        data = {}
        data['ticker'] = self.ticker
        data['buys'] = self.buys
        data['sells'] = self.sells
        data['orders'] = self.orders
        data['starting_balance'] = self.starting_balance
        data['ending_balance'] = self.ending_balance
        
        return json.dumps(data)
    
    def __str__(self):
        return self.json()

    def printResult(self):
        print("=======================================")
        print("Summary Statistics ({}):".format(self.ticker))
        print("=======================================")
        print("Number of Buys: {}".format(len(self.buys)))
        print("Number of Sells: {}".format(len(self.sells)))
        print("Starting Balance: {:.2f}".format(self.starting_balance))
        print("Ending Balance: {:.2f}".format(self.ending_balance))
        print("=======================================")
