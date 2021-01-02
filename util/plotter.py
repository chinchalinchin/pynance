import numpy, matplotlib
from PIL import Image

from matplotlib import pyplot as plot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import app.settings as settings

matplotlib.use("Qt5Agg")

def plot_frontier(portfolio, frontier, show=True, savefile=None):
    return_profile=[]
    risk_profile=[]
    for allocation in frontier:
        return_profile.append(portfolio.return_function(allocation))
        risk_profile.append(portfolio.volatility_function(allocation))
    return_profile = numpy.array(return_profile)
    risk_profile = numpy.array(risk_profile)
    
    title = " ( "
    for i in range(len(portfolio.tickers)):
        if i != (len(portfolio.tickers) - 1):
            title += portfolio.tickers[i] + ", "
        else:
            title += portfolio.tickers[i] + " ) Efficient Frontier"
    
    canvas = FigureCanvas(Figure())
    axes = canvas.figure.subplots()

    axes.plot(risk_profile, return_profile, linestyle='dashed')
    axes.set_xlabel('Volatility')
    axes.set_ylabel('Return')
    axes.set_title(title)

    if savefile is not None:
        canvas.print_jpeg(filename_or_obj=savefile)

    if show:
        s, (width, height) = canvas.print_to_buffer()
        im = Image.frombytes("RGBA", (width, height), s)
        im.show()
    else:
        return canvas

def plot_profiles(symbols, profiles):
    canvas = FigureCanvas(Figure())

    x = numpy.arange(len(symbols))
    axes = canvas.figure.subplots()

def plot_moving_averages(symbols, averages, show=True, savefile=None):
    canvas = FigureCanvas(Figure())

    width = settings.BAR_WIDTH
    x = numpy.arange(len(symbols))
    axes = canvas.figure.subplots()
    
    ma1s, ma2s, ma3s = [], [], []
    for i in range(len(symbols)):
        ma1s.append(averages[i][0])
        ma2s.append(averages[i][1])
        ma3s.append(averages[i][2])
    
    ma1_label, ma2_label, ma3_label = f'MA({settings.MA_1_PERIOD})', f'MA({settings.MA_2_PERIOD})', f'MA({settings.MA_3_PERIOD})'

    axes.bar(x + width, ma1s, width, label=ma1_label)
    axes.bar(x, ma2s, width, label=ma2_label)
    axes.bar(x - width, ma3s, width, label=ma3_label)

    axes.set_ylabel('Moving Average of Daily Return')
    axes.set_title('Moving Averages of Daily Return Grouped By Equity')
    axes.set_xticks(x)
    axes.set_xticklabels(symbols)
    axes.legend()

    if savefile is not None:
        canvas.print_jpeg(filename_or_obj=savefile)

    if show:
        s, (width, height) = canvas.print_to_buffer()
        im = Image.frombytes("RGBA", (width, height), s)
        im.show()
    else:
        return canvas