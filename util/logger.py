import datetime
import numpy as numpy
import matplotlib.pyplot as matplotlib

import app.settings as settings

import util.helpers as helper


class Logger():

    def __init__(self, location):
        self.location = location
    
    def comment(self, msg):
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print(dt_string, ' :' , self.location, ' : ',msg)

    def return_line(self):
        print('\n')

    def break_lines(self, msg):
        if len(msg)>settings.LINE_LENGTH:
            return [msg[i:i+settings.LINE_LENGTH] for i in range(0,len(msg), settings.LINE_LENGTH)]
        else:
            return [msg]

    def debug(self, msg):
        if settings.DEBUG:
            self.comment(msg)

    def title_line(self, title):
        buff = int((settings.LINE_LENGTH - len(title))/2)
        print(settings.SEPARATER*buff, title, settings.SEPARATER*buff) 
    
    def line(self):
        print(settings.SEPARATER*settings.LINE_LENGTH)

    def center(self, this_line):
        buff = int((settings.LINE_LENGTH - len(this_line))/2)
        print(' '*buff, this_line, ' '*buff)

    def example_expo(self, ex_no, example, explanation):
        print(' '*settings.INDENT, f'#{ex_no}:', example)
        for line in self.break_lines(explanation):
            print(' '*2*settings.INDENT, '-', line)

    def examples(self):
        index = 1
        for example in settings.EXAMPLES:
            self.example_expo(index, example, settings.EXAMPLES[example])
            self.return_line()
            index += 1

    def scalar_result(self, calculation, result):
        print(' '*settings.INDENT, '>>', calculation, ' = ', round(result, 4))

    def portfolio_percent_result(self, result, tickers):
        for i in range(len(tickers)):
            print(' '*settings.INDENT, f'{tickers[i]} =', round(100*result[i], 2), '%')

    def portfolio_shares_result(self, result, tickers):
        for i in range(len(tickers)):
            print(' '*settings.INDENT, f'{tickers[i]} =', result[i])

    def option(self, opt, explanation):
        print(' '*settings.INDENT, opt, " :")
        for line in self.break_lines(explanation):
            print(' '*settings.INDENT*2, line)

    def optimal_result(self, portfolio, allocation):
        self.title_line('Optimal Percentage Allocation')
        self.portfolio_percent_result(allocation, portfolio.tickers)
        self.line()

        if settings.INVESTMENT_MODE:
            investment = helper.get_number_input("Please Enter Total Investment : \n")
            shares = portfolio.calculate_approximate_shares(allocation, investment)
            total = portfolio.calculate_actual_total(allocation, investment)
            
            self.line()
            self.title_line('Optimal Share Allocation')
            self.portfolio_shares_result(shares, portfolio.tickers)
            self.title_line('Optimal Portfolio Value')
            self.scalar_result('Total', round(total,2))

        self.title_line('Risk-Return Profile')
        self.scalar_result('Return', portfolio.return_function(allocation))
        self.scalar_result('Volatility', portfolio.volatility_function(allocation))

    def efficient_frontier(self, portfolio, frontier):
        if settings.INVESTMENT_MODE:
            investment = helper.get_number_input("Please Enter Total Investment : \n")
        else:
            investment = 1000
        
        self.title_line(f'(Annual Return %, Annual Volatility %) Portfolio')

        for allocation in frontier:
            self.line()
            return_string=str(round(round(portfolio.return_function(allocation),4)*100,2))
            vol_string=str(round(round(portfolio.volatility_function(allocation),4)*100,2))
            self.title_line(f'({return_string} %, {vol_string}%) Portfolio')
            self.line()

            self.title_line('Optimal Percentage Allocation')

            self.portfolio_percent_result(allocation, portfolio.tickers)
            
            if settings.INVESTMENT_MODE:
                shares = portfolio.calculate_approximate_shares(allocation, investment)
                total = portfolio.calculate_actual_total(allocation, investment)
            
                self.title_line('Optimal Share Allocation')
                self.portfolio_shares_result(shares, portfolio.tickers)
                self.title_line('Optimal Portfolio Value')
                self.scalar_result('Total', round(total,2))
            
            self.title_line('Risk-Return Profile')
            self.scalar_result('Return', portfolio.return_function(allocation))
            self.scalar_result('Volatility', portfolio.volatility_function(allocation))
            self.return_line()

    def plot_frontier(self, portfolio, frontier):
        return_profile=[]
        risk_profile=[]
        for allocation in frontier:
            return_profile.append(portfolio.return_function(allocation))
            risk_profile.append(portfolio.volatility_function(allocation))
        return_profile = numpy.array(return_profile)
        risk_profile = numpy.array(risk_profile)
        
        title = " ( "
        index = 0
        for ticker in portfolio.tickers:
            if index != (len(portfolio.tickers) - 1):
                title += ticker + ", "
                index += 1
            else:
                title += ticker + " ) Efficient Frontier"
        
        matplotlib.plot(risk_profile, return_profile, linestyle='dashed')
        matplotlib.xlabel('Volatility')
        matplotlib.ylabel('Return')
        matplotlib.title(title)
        matplotlib.show()

    def help(self):
        self.title_line(settings.APP_NAME)
        explanation=self.break_lines(settings.HELP_MSG)
        for line in explanation:
            self.center(line)
        self.return_line()

        self.title_line('SYNTAX')
        self.center(settings.SYNTAX)
        self.return_line()

        self.title_line('OPTIONS')
        options = settings.FUNC_ARG_DICT.keys()
        for option in options:
            self.option(settings.FUNC_ARG_DICT[option], settings.FUNC_DICT[option])
            self.return_line()