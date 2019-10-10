# analysis file 'analysis.py': a file for analysis of things to be analyzed

def total_profit(results):
    '''
    Return total profits across all tests

    Params
    ------
    results : list
        List of dictionaries containing testing results.
    Returns
    -------
    profit : float
        Total profit across all tests
    '''
    profit = 0

    for result in results:
        profit += result["ending_balance"] - result["starting_balance"]
    
    return profit

def profit_per_unit_time(results):
    pass

# Calculate the largest downfall from a peak to a trough
def largest_drawdown(results):
    pass 

# Calculate the longest period of time a strategy didn't reach a new high
def longest_drawdown(results):
    pass
    # Store the initial price
        # the time it was reached
        # the amount of its value
    # Once the current value is >= the peak, return the time-difference 
        # Return as a pendulum time delta
    pass


'''
Portfolio 1
    Strategy 1
        Stock 1
        Stock 2
        Stock 3
    Strategy 2
        Stock 1
        Stock 4
        Stock 5
'''

'''
Stock 1, buy
STock 2, buy
Stock 3, buy
Portfolio, 
'''