# Xylem Testing Platform
Xylem is a simple backtesting platform developed for Splay Tree Capital. To write a xylem compatible algorithm, you need two files. A python file containing the algorithm code and a YAML file containing the algorithm's testing configuration.

## Install Xylem
Xylem is currently a proprietary library of Splay Tree Capital. If you're reading this, you're probably an employee on gitlab. To install Xylem, clone the repository and run the following command:

```
pip install -e /path/to/xylem/directory
```
Xylem is now installed on your local machine. Any unauthorized release of Xylem to third parties is in violation of the non-disclosure agreement.
## Run Xylem


```
Xylem. A backtesting platform...

Usage:
  xylem run -a ALGORITHM
  xylem (-h | --help)
  xylem --version

Options:
  -h --help                     Show this screen.
  -v --version                  Show version.
  -a --algorithm ALGORITHM      Path to algorithm configuration file.
```

To run the sample algorithm provided below, issue the following command:
```
xylem run -a /path/to/algorithm/config/file
```
## Sample Algorithm
### Algorithm File
```python
def compute(context, stats, order):
    # If short term momentum exceeds long term momentum
    if (stats["EMA12"] * (1.00 - context["bias"])) > stats["EMA26"] and not context["long_position"]:
        # Enter a long position, selling our short position if we have one
        if context["short_position"]:
            # Returning the stock that we borrowed requires subtracting from our balance
            order(1)
            context["short_position"] = False

        order(1)
        context["long_position"] = True
        
    # If short term momentum falls below long term momentum
    elif (stats["EMA12"] * (1.00 + context["bias"])) < stats["EMA26"] and not context["short_position"]:
        # Enter a short position, selling our long position if we have one
        if context["long_position"]:
            order(-1)
            context["long_position"] = False

        order(-1)
        context['short_position'] = True

def before_exit(context, stats, order):
    if context["long_position"]:
        print("Long position before_exit()")
        order(liquidate=True)

    if context["short_position"]:
        print("Short position before_exit()")
        order(1)

def analyze(result_set):
  for result in result_set:
    print(result.json())
```

Xylem will execute each function at different points in the testing lifecycle. The following lifecycle functions are available in xylem:

* **compute**: This is where the main algorithm code lives. This function represents a single computational step of your algorithm. You are given a context dictionary which remains static on each step. Additionally, you are given a stats dictionary containing the data required for your algorithm to make a decision. You are also provided with an ``` order ``` function to buy and sell virtual currency. Context and stats are configurable by adjusting the YAML file accordingly.
* **before_exit**: This function is executed once before exiting the training phase.
* **analyze**: This function is called at the end of the training phase with your algorithm's results.

### Configuration File
```yaml
algorithm: /Users/austin/splay_tree/macd/algorithm.py
output: /Users/austin/splay_tree/macd/test_output
equity: 25000
context:
  long_position: false
  short_position: false
  bias: 0.0
statistics:
  - EMA12
  - EMA26
tests:
  - TEST AAPL,AMD AT RANDOM FROM 2019-06-21 TO 2019-06-23 DURATION 5 MONTHS ATTEMPT 5 TIMES
  - TEST V,TSLA AT RANDOM FROM 2019-02-21 TO 2019-05-21 DURATION 1 MONTH ATTEMPT 3 TIMES
```

Here is a sample YAML file corresponding to the sample algorithm given above. The following configuration parameters are available:

* **algorithm**: Path to the algorithm python file.
* **output**: Path to the directory where testing output will be stored.
* **equity**: Equity available at the beginning of each training phase. In other words, the amount of money your algorithm can lose. 
* **context**: This is a dictionary of context parameters. You can add any parameter you would like (along with its initial condition) and it will be available in the context argument described above.
* **statistics**: A list of statistics available at each computational step of your algorithm. Currently supported statistics:
    * EMA12
    * EMA26
* **tests**: Xylem implements a SQL-like syntax for defining each training phase you would like to run. See the xylang section for more details.

## Xylang
Xylang is a SQL-like syntax for defining testing phases for your algorithm. The following commands are available in xylang:
* ``` TEST <ticker> ``` This command tells Xylem which tickers you would like to test your algorithm on. For example, you might say ``` TEST AAPL ``` for a single ticker, ``` TEST AAPL,AMD ``` for multiple tickers, or ```TEST *``` for all tickers.
* ``` AT RANDOM ``` Adding this command tells Xylem that you would like to randomly select dates from the provided range. The default action is to begin from the start and proceed sequentially.
* ``` FROM <begin> TO <end> ``` This tells Xylem the date range on which you would like to test your algorithm. 
* ``` DURATION <duration> ``` This tells Xylem the duration for the test. For example, one might say ``` DURATION 5 MONTHS``` which will instruct xylem to test in 5 month increments selected from the given date range.
* ``` ATTEMPT <attemps> ``` This tells Xylem how many times you would like to test the algorithm. For example, ``` ATTEMPT 5 TIMES ``` instructs Xylem to test the algorithm 5 times on different intervals in the date range.
