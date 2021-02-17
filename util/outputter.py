import datetime, sys

import util.helper as helper
import util.formatter as formatter

LOG_LEVEL_NONE = "none"
LOG_LEVEL_INFO = "info"
LOG_LEVEL_DEBUG = "debug"
LOG_LEVEL_VERBOSE = "verbose"

def print_below_new_line(msg):
    print(f'\n{msg}')

def title_line(title):
    buff = int((formatter.LINE_LENGTH - len(title))/2)
    print(formatter.SEPARATER*buff, title, formatter.SEPARATER*buff) 
    
def line():
    print(formatter.SEPARATER*formatter.LINE_LENGTH)

def return_line():
    print('\n')

def break_lines(msg):
    if len(msg)>formatter.LINE_LENGTH:
        return [msg[i:i+formatter.LINE_LENGTH] for i in range(0,len(msg), formatter.LINE_LENGTH)]
    else:
        return [msg]

def center(this_line):
    buff = int((formatter.LINE_LENGTH - len(this_line))/2)
    print(' '*buff, this_line, ' '*buff)

def print_list(list_to_print):
    for i in range(len(list_to_print)):
        print(formatter.TAB, f'{i}. {list_to_print[i]}')

def string_result(operation, result):
    print(' '*formatter.INDENT, '>>', operation, ' = ', result)
        
def scalar_result(calculation, result, currency=True):
    if currency:
        print(' '*formatter.INDENT, '>>', calculation, ' = $', round(result, 2))
    else:
        print(' '*formatter.INDENT, '>>', calculation, ' = ', round(result, 4))

def equivalent_result(right_hand, left_hand, value):
    print(' '*formatter.INDENT, '>>', f'{right_hand} = {left_hand} = {value}')

def portfolio_percent_result(result, tickers):
    for i in range(len(tickers)):
        print(' '*formatter.INDENT, f'{tickers[i]} =', round(100*result[i], 2), '%')

def portfolio_shares_result(result, tickers):
    for i in range(len(tickers)):
        print(' '*formatter.INDENT, f'{tickers[i]} =', result[i])

def example(ex_no, example, explanation):
    print(' '*formatter.INDENT, f'#{ex_no}:', example)
    for line in break_lines(explanation):
        print(' '*2*formatter.INDENT, '-', line)

def examples():
    index = 1
    for ex in formatter.EXAMPLES:
        example(index, ex, formatter.EXAMPLES[ex])
        return_line()
        index += 1
    
def option(opt, explanation):
    print(' '*formatter.INDENT, opt, " :")
    for line in break_lines(explanation):
        print(' '*formatter.INDENT*2, line)

def help():
    title_line(formatter.APP_NAME)
    explanation=break_lines(formatter.HELP_MSG)
    for line in explanation:
        center(line)
    return_line()

    title_line('SYNTAX')
    center(formatter.SYNTAX)
    return_line()

    title_line('OPTIONS')
    options = formatter.FUNC_ARG_DICT.keys()
    for option in options:
        option(formatter.FUNC_ARG_DICT[option], formatter.FUNC_DICT[option])
        return_line()
 # APPLICATION SPECIFIC FORMATTING FUNCTIONS

def spot_price(ticker, spot_price):
    formatted_price = round(float(spot_price), 2)
    scalar_result(f'{ticker} spot price', formatted_price)
    
def model_price(ticker, model_price, model):
    formatted_price = round(float(model_price),2)
    scalar_result(f'{ticker} {str(model).upper()} price', formatted_price)

def moving_average_result(tickers, averages_output, periods, start_date = None, end_date = None):
    averages, dates = averages_output
    MA1_prefix, MA2_prefix, MA3_prefix = f'MA({periods[0]})', f'MA({periods[1]})', f'MA({periods[2]})'
    if start_date is None and end_date is None:
        for i in range(len(tickers)):
            title = f'{tickers[i]} Moving Average of Daily Return for {periods[0]}, {periods[1]} & {periods[0]} Days'
            title_line(title)

            MA1_title, MA2_title, MA3_title = f'{MA1_prefix}_{tickers[i]}', f'{MA2_prefix}_{tickers[i]}', f'{MA3_prefix}_{tickers[i]}'
            scalar_result(MA1_title, round(averages[i][0], 2))
            scalar_result(MA2_title, round(averages[i][1], 2))
            scalar_result(MA3_title, round(averages[i][2], 2))
    else:
        for i in range(len(tickers)):

            title = f'{tickers[i]} Moving Average of Daily Return for {periods[0]}, {periods[1]} & {periods[0]} Days'
            title_line(title)

            MA1_title, MA2_title, MA3_title = f'{MA1_prefix}_{tickers[i]}', f'{MA2_prefix}_{tickers[i]}', f'{MA3_prefix}_{tickers[i]}'
            count = 0
            for j in range(len(dates)):
                msg_1 = f'{dates[j]} : {MA1_title}'
                scalar_result(msg_1, round(averages[i][0][j], 2))
            for j in range(len(dates)):
                msg_2 = f'{dates[j]} : {MA2_title}'
                scalar_result(msg_2, round(averages[i][1][j], 2))
            for j in range(len(dates)):  
                msg_3 = f'{dates[j]} : {MA3_title}'
                scalar_result(msg_3, round(averages[i][2][j], 2))      

def screen_results(info, model):
    for ticker in info:
        title_line(f'{ticker} {str(model).upper()} Model vs. Spot Price ')
        spot_price(ticker=ticker, spot_price=info[ticker]['spot_price'])
        model_price(ticker=ticker, model_price=info[ticker]['model_price'], model=model)
        scalar_result(f'{ticker} discount', info[ticker]['discount'])
        line()

# TODO: parse investment argument from command line instead of getting number input like this.
# TODO: can probably combine optimal_result and efficient_frontier into a single function
#         by wrapping the optimal_results in an array so when it iterates through frontier
#         in efficient_frontier, it will only pick up the single allocation array for the
#         optimal result.
def optimal_result(portfolio, allocation, user_input):
    title_line('Optimal Percentage Allocation')
    portfolio_percent_result(allocation, portfolio.tickers)
    line()

    if user_input:
        investment = helper.get_number_input("Please Enter Total Investment : \n")
        shares = portfolio.calculate_approximate_shares(allocation, investment)
        total = portfolio.calculate_actual_total(allocation, investment)
        
        line()
        title_line('Optimal Share Allocation')
        portfolio_shares_result(shares, portfolio.tickers)
        title_line('Optimal Portfolio Value')
        scalar_result('Total', round(total,2))

    title_line('Risk-Return Profile')
    scalar_result(calculation='Return', result=portfolio.return_function(allocation), currency=False)
    scalar_result(calculation='Volatility', result=portfolio.volatility_function(allocation), currency=False)

def efficient_frontier(portfolio, frontier, user_input):
    if user_input:
        investment = helper.get_number_input("Please Enter Total Investment : \n")
    else:
        investment = 1000
    
    title_line(f'(Annual Return %, Annual Volatility %) Portfolio')
    # TODO: edit title to include dates

    for allocation in frontier:
        line()
        return_string=str(round(round(portfolio.return_function(allocation),4)*100,2))
        vol_string=str(round(round(portfolio.volatility_function(allocation),4)*100,2))
        title_line(f'({return_string} %, {vol_string}%) Portfolio')
        line()

        title_line('Optimal Percentage Allocation')

        portfolio_percent_result(allocation, portfolio.tickers)
        
        if user_input:
            shares = portfolio.calculate_approximate_shares(allocation, investment)
            total = portfolio.calculate_actual_total(allocation, investment)
        
            title_line('Optimal Share Allocation')
            portfolio_shares_result(shares, portfolio.tickers)
            title_line('Optimal Portfolio Value')
            scalar_result('Total', round(total,2))
        
        title_line('Risk-Return Profile')
        scalar_result('Return', portfolio.return_function(allocation))
        scalar_result('Volatility', portfolio.volatility_function(allocation))
        return_line()
        
class Logger():

    def __init__(self, location, log_level="info"):
        self.location = location
        self.log_level = log_level
    
    # LOGGING FUNCTIONS
    def comment(self, msg):
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(dt_string, ' :' , self.location, ' : ',msg)

    def info(self, msg):
        if self.log_level in [LOG_LEVEL_INFO, LOG_LEVEL_DEBUG, LOG_LEVEL_VERBOSE]:
            self.comment(msg)

    def debug(self, msg):
        if self.log_level in [LOG_LEVEL_DEBUG, LOG_LEVEL_VERBOSE]:
            self.comment(msg)

    def verbose(self, msg):
        if self.log_level == LOG_LEVEL_VERBOSE:
            self.comment(msg)
            
    def sys_error(self):
        e, f, g = sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]
        msg = f'{e} \n {f} \n {g} \n'
        self.debug(msg)

    def log_arguments(self, main_args, xtra_args, xtra_values):
        self.debug(f'Main Arguments: {main_args}')
        for i in range(len(xtra_args)):
            if i < len(xtra_values):
                self.debug(f'Extra Argument: {xtra_args[i]} = {xtra_values[i]}')
            else:
                self.debug(f'Extra Argument: {xtra_args[i]}')

    def log_django_settings(self, settings):
            line()
            self.title_line('SETTINGS.PY Configuration')
            line()
            self.debug("# Environment Configuration")
            self.debug(f'> Directory Location : {settings.BASE_DIR}')
            self.debug(f'> Environment: {settings.APP_ENV}')
            line()
            self.debug("# Application Configuration")
            self.debug(f'> Debug : {settings.DEBUG}')
            self.debug(f'> Enviroment: {settings.APP_ENV}')
            self.debug(f'> Log Level: {settings.LOG_LEVEL}')
            line()
            self.debug("# Database Configuration")
            self.debug(f'> Database Engine: {settings.DATABASES["default"]["ENGINE"]}')
            line()