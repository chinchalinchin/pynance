# Pynance: A Financial Optimization Application

## Prerequisites
- [Python 3.8 +](https://www.python.org/downloads/) <br>
- [NodeJS](https://nodejs.org/en/download/)<br>
- [PostgreSQL](https://www.postgresql.org/download/)<br>
- [Docker](https://www.docker.com/products/docker-desktop)<br>

This is a financial application that calculates asset correlations, statistics and optimal portfolio allocations using data it retrieves from external services (currently: [AlphaVantage](https://www.alphavantage.co), [IEX](https://iexcloud.io/) and [Quandl](https://www.quandl.com/)). Statistics are calculated using [Ito Calculus](https://en.wikipedia.org/wiki/It%C3%B4_calculus) and should be consistent with the results demanded by [Modern Portfolio Theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory) and [Financial Engineering](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_equation). The portfolios are optimized by minimizing the portfolio's variance/volatility, i.e. by finding the optimal spot on the portfolio's efficient frontier as defined by the [CAPM model](https://en.wikipedia.org/wiki/Capital_asset_pricing_model), or alternatively, by maximizing the portfolio's [Sharpe ratio](https://en.wikipedia.org/wiki/Sharpe_ratio).

The program's functions are wrapped in [PyQt5](https://doc.qt.io/qtforpython/index.html) widgets which provide a user interface. In addition, visualizations are created by [matplotlib](https://matplotlib.org/3.3.3/contents.html) for easier presentation.

See [CLI Application Setup](cli-application/SETUP.md) for more information on setting up the CLI.

The program's functions can also be wired into a WSGI Application using the [Django framework](https://docs.djangoproject.com/en/3.1/) provided in the <i>/server/</i> directory. See <b>[WSGI Application](wsgi-application/SERVER.md)</b> for more information. The WSGI application can be containerized using the <i>Dockerfile</i> in the project root and deployed as a microservice. An [Angular](https://angular.io/docs) frontend can be built and served up through an <b>[nginx](https://nginx.org/en/docs/)</b> container to provide a user interface for the backend service. See [WSGI Container](wsgi-application/CONTAINER.md) and [Frontend](wsgi-application/FRONTEND.md) for more information.

See [Setup](main/SETUP.md) for more information setting the application for the first time. See [Environment](main/configuration/ENVIRONMENT.md) for more information on configuration options. See [Examples](main/EXAMPLES.md) for example usage of the application.

This documentation was generated using [Sphinx](https://www.sphinx-doc.org/en/master/).