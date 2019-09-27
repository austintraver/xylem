import json

class Result:
    def __init__(self, ticker, orders, starting_balance, ending_balance, start_time, stop_time):
        self.ticker = ticker
        self.orders = orders
        self.starting_balance = starting_balance
        self.ending_balance = ending_balance
        self.start_time = start_time
        self.stop_time = stop_time

    def json(self):
        data = {}
        data['ticker'] = self.ticker
        data['orders'] = self.orders
        data['starting_balance'] = self.starting_balance
        data['ending_balance'] = self.ending_balance
        data['start_time'] = self.start_time
        data['stop_time'] = self.stop_time

        return json.dumps(data)

    def __str__(self):
        return self.json()

    def printResult(self):
        print("=======================================")
        print("Summary Statistics ({}):".format(self.ticker))
        print("=======================================")
        print("Start Time: {}".format(self.start_time))
        print("Stop Time: {}".format(self.stop_time))
        print("Starting Balance: {:.2f}".format(self.starting_balance))
        print("Ending Balance: {:.2f}".format(self.ending_balance))
        print("=======================================")
