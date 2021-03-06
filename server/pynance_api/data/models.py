from django.db import models

import app.settings as app_settings
import app.util.helper as helper


# Have to separate equity and crypto tickers since GLD exists in both
# crypto and equity symbols. Real pain.
class EquityTicker(models.Model):
    ticker = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.ticker

class CryptoTicker(models.Model):
    ticker = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.ticker

class StatSymbol(models.Model):
    symbol = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.symbol

class EquityMarket(models.Model):
    ticker = models.ForeignKey(EquityTicker, on_delete=models.CASCADE)
    date = models.DateField('Date')
    open_price = models.DecimalField(max_digits=20, decimal_places=4)
    close_price = models.DecimalField(max_digits=20, decimal_places=4)
    
    def __str__(self):
        return '{} {} : {}'.format(self.ticker, self.date, self.close_price)
    
    # TODO: may need to change AV_RES_EQUITY_CLOSE_PRICE key to something more generalized.
    def to_dict(self):
        formatted_self = {}
        formatted_self[app_settings.AV_RES_EQUITY_OPEN_PRICE] = float(self.open_price)
        formatted_self[app_settings.AV_RES_EQUITY_CLOSE_PRICE] = float(self.close_price) 
        return formatted_self
    
    def to_date(self):
        return helper.date_to_string(self.date)

class EquityProfileCache(models.Model):
    ticker = models.ForeignKey(EquityTicker,on_delete=models.CASCADE)
    start_date = models.DateField('Start Date')
    end_date = models.DateField('End Date')
    annual_return = models.DecimalField(max_digits=20, decimal_places=6, null=True)
    annual_volatility = models.DecimalField(max_digits=20, decimal_places=6, null=True)
    sharpe_ratio = models.DecimalField(max_digits=20, decimal_places=6, null=True)
    asset_beta = models.DecimalField(max_digits=20, decimal_places=6, null=True)

class EquityCorrelationCache(models.Model):
    ticker_1 = models.ForeignKey(EquityTicker, on_delete=models.CASCADE, related_name="ticker_1")
    ticker_2 = models.ForeignKey(EquityTicker, on_delete=models.CASCADE, related_name="ticker_2")
    start_date = models.DateField('Start Date')
    end_date = models.DateField('End Date')
    correlation = models.DecimalField(max_digits=20, decimal_places=6, null=True)
    
class Dividends(models.Model):
    ticker = models.ForeignKey(EquityTicker, on_delete=models.CASCADE)
    date = models.DateField('Payment Date')
    amount = models.DecimalField(max_digits=20, decimal_places=4)

    def __str__(self):
        return '{} {}: {}'.format(self.ticker, self.date, self.amount)

    # TODO: may need to change IEX_RES_DIV_KEY key to something more generalized.
    def to_dict(self):
        return float(self.amount)
    
    def to_date(self):
        return helper.date_to_string(self.date)

class CryptoMarket(models.Model):
    ticker = models.ForeignKey(CryptoTicker, on_delete=models.CASCADE)
    date = models.DateField('Date')
    open_price = models.DecimalField(max_digits=20, decimal_places=10)
    close_price = models.DecimalField(max_digits=20, decimal_places=10)
    
    def __str__(self):
        return '{} {} : {}'.format(self.ticker, self.date, self.closing_price)
    
    def to_dict(self):
        formatted_self = {}
        formatted_self[app_settings.AV_RES_CRYPTO_OPEN_PRICE] = float(self.open_price)
        formatted_self[app_settings.AV_RES_CRYPTO_CLOSE_PRICE] = float(self.close_price) 
        return formatted_self

    def to_date(self):
        return helper.date_to_string(self.date)

class Economy(models.Model):
    statistic = models.ForeignKey(StatSymbol, max_length=10, on_delete=models.CASCADE)
    date = models.DateField('Date')
    value = models.DecimalField(max_digits=20, decimal_places=10)
    
    def __str__(self):
        return '{} {} : {}'.format(self.statistic, self.date, self.value)