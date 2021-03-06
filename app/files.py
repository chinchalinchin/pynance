"""
Description
-----------
`app.files` is in charge of all application file handling. In addition, this module handles requests for large csv files retrieved from external services. The metadata files from 'AlphaVantage' and 'Quandl' are returned as zipped csv files. The functions within in this module perform all the tasks necessary for parsing this response into the application file system, whether on the localhost or a containerized filesytem.
"""
import os, io, json, datetime, csv, zipfile
import requests

import app.settings as settings

import app.util.outputter as outputter
import app.util.helper as helper

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

CLOSE_PRICE = "close"
OPEN_PRICE = "open"

OBJECTS={
    "correlation": 1,
    "risk_profile": 2,
    "prices": 3,
    "dividends": 4,
    "statistic": 5,
}
logger = outputter.Logger("app.files", settings.LOG_LEVEL)

def determine_analysis_date_range(start_date=None, end_date=None):
    if end_date is None:
        end_date = helper.get_previous_business_date(date=helper.get_today())
    if start_date is None:
        start_date = helper.decrement_date_by_business_days(end_date, settings.DEFAULT_ANALYSIS_PERIOD)
    return start_date, end_date

def generate_timestamp(args):
    start_date = args.get('start_date')
    end_date = args.get('end_date')
    start_date, end_date = determine_analysis_date_range(start_date=start_date, end_date=end_date)
    timestamp = '{}_{}'.format(helper.date_to_string(start_date),helper.date_to_string(end_date))
    return timestamp

def load_file(file_name):
    with open(file_name, 'r') as infile:
        if settings.FILE_EXT == "json":
            prices = json.load(infile)
        return prices
        # TODO: implement other file loading extensions

def save_file(file_to_save, file_name):
    with open(file_name, 'w') as outfile:
        if settings.FILE_EXT == "json":
            try:
                json.dump(file_to_save, outfile)
                return True
            except:
                return False
        # TODO: implement other file saving extensions.

def store_local_object(local_object, value, args):
    if settings.LOCAL_CACHE:
        timestamp = generate_timestamp(args=args)
        
        if local_object == OBJECTS['correlation']:
            # TODO: save second file 
            logger.debug(f'Storing ({args["ticker_1"]}, {args["ticker_2"]}) correlation in local cache.')
            file_name = f'{timestamp}_{args["ticker_1"]}_{args["ticker_2"]}_{settings.CACHE_COR_KEY}.{settings.FILE_EXT}'
            file_name_2 = f'{timestamp}_{args["ticker_2"]}_{args["ticker_1"]}_{settings.CACHE_COR_KEY}.{settings.FILE_EXT}'
        if local_object == OBJECTS['prices']:
            logger.debug(f'Storing {args["ticker"]} price history in local cache.')
            file_name = f'{timestamp}_{args["ticker"]}_{settings.CACHE_PRICE_KEY}.{settings.FILE_EXT}'
        if local_object == OBJECTS['risk_profile']:
            logger.debug(f'Storing {args["ticker"]} risk profile in local cache.')
            file_name = f'{timestamp}_{args["ticker"]}_{settings.CACHE_PRO_KEY}.{settings.FILE_EXT}'
        if local_object == OBJECTS['dividends']:
            logger.debug(f'Checking for {args["ticker"]} dividend history in local cache.')
            file_name = os.path.join(settings.CACHE_DIR, f'{timestamp}_{args["ticker"]}_{settings.CACHE_DIV_KEY}.{settings.FILE_EXT}')
        if local_object == OBJECTS['statistic']:
            file_name = os.path.join(settings.CACHE_DIR, f'{timestamp}_{args["stat_symbol"]}_{settings.CACHE_STAT_KEY}.{settings.FILE_EXT}')

        buffer_store= os.path.join(settings.CACHE_DIR, file_name)
        return save_file(file_to_save=value, file_name=buffer_store)
    return False

def retrieve_local_object(local_object, args):
    if settings.LOCAL_CACHE:
        timestamp = generate_timestamp(args=args)
        
        if local_object == OBJECTS['correlation']:
            buffer_store_1= os.path.join(settings.CACHE_DIR, f'{timestamp}_{args["ticker_1"]}_{args["ticker_2"]}_{settings.CACHE_COR_KEY}.{settings.FILE_EXT}')
            buffer_store_2= os.path.join(settings.CACHE_DIR, f'{timestamp}_{args["ticker_2"]}_{args["ticker_1"]}_{settings.CACHE_COR_KEY}.{settings.FILE_EXT}')

            logger.debug(f'Checking for ({args["ticker_1"]}, {args["ticker_2"]}) correlation calculation in local cache.')
            if os.path.isfile(buffer_store_1):
                logger.debug(f'Loading in cached ({args["ticker_1"]}, {args["ticker_2"]}) correlation.')
                correlation = load_file(file_name=buffer_store_1)
                return correlation
            elif os.path.isfile(buffer_store_2):
                logger.debug(f'Loading in cached ({args["ticker_2"]}, {args["ticker_1"]}) correlation.')
                correlation = load_file(file_name=buffer_store_2)
                return correlation
            return None

        elif local_object == OBJECTS['risk_profile']:
            file_name = os.path.join(settings.CACHE_DIR, f'{timestamp}_{args["ticker"]}_{settings.CACHE_PRO_KEY}.{settings.FILE_EXT}')
            logger.debug(f'Checking for {args["ticker"]} statistics in local cache.')
            if os.path.isfile(file_name):
                results = load_file(file_name=file_name)
                return results
        
        elif local_object == OBJECTS['prices']:
            # TODO: with different time stamp implementation, this part of the method should search for price histories that contain
            # the range in start_date and end_date.

            # start_date, end_date = args.get('start_date'), args.get('end_date')
            # start_date, end_date = determine_analysis_date_range(start_date, end_date)

            # for file in path(settings.CACHE_DIR) or whatever:
                # key_check = f'{args["ticker"]}_{settings.CACHE_PRICE_KEY}'
                # if key_check in file.name:
                    # components = file.name.split('_')
                    # cached_start_date = parsed_date(components[0])
                    # cached_end_date = parsed_date(components[1])
                    
                    # if cached_start_date <= start_date and cached_end_date >= end_date:
                        # parsed start_date to end_date from cached_prices

            file_name = os.path.join(settings.CACHE_DIR, f'{timestamp}_{args["ticker"]}_{settings.CACHE_PRICE_KEY}.{settings.FILE_EXT}')
            logger.debug(f'Checking for {args["ticker"]} prices in local cache.')
            if os.path.isfile(file_name):
                results = load_file(file_name=file_name)
                return results

        elif local_object == OBJECTS['statistic']:
            file_name = os.path.join(settings.CACHE_DIR, f'{timestamp}_{args["stat_symbol"]}_{settings.CACHE_STAT_KEY}.{settings.FILE_EXT}')
            logger.debug(f'Checking for {args["stat_symbol"]} statistics in cache')
            if os.path.isfile(file_name):
                results = load_file(file_name=file_name)
                return results

    return None

def parse_csv_response_column(column, url, firstRowHeader=None, savefile=None, zipped=None):
    """
    Parameters
    ----------
    1. column : int \n
        Required. Index of the column you wish to retrieve from the response. \n \n
    2. url : str \n
        Required. The url, already formatted with appropriate query and key, that will respond with the csv file, zipped or unzipped (see zipped argument for more info), you wish to parse. \n \n 
    3. firstRowHeader : str \n 
        Optional. name of the header for the column you wish to parse. if specified, the parsed response will ignore the row header. Do not include if you wish to have the row header in the return result. \n \n 
    4. savefile : str \n 
        Optional. the absolute path of the file you wish to save the parsed response column to. \n \n 
    5. zipped : str \n 
        if the response returns a zip file, this argument needs to be set equal to the file within the zipped archive you wish to parse. \n \n 
    """
    col, big_mother = [], []

    with requests.Session() as s:
        download = s.get(url)
        
        if zipped is not None:
            zipdata = io.BytesIO(download.content)
            unzipped = zipfile.ZipFile(zipdata)
            with unzipped.open(zipped, 'r') as f:
                for line in f:
                    big_mother.append(helper.replace_troublesome_chars(line.decode("utf-8")))
                cr = csv.reader(big_mother, delimiter=',')
        
        else:
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')

        s.close()
    
    for row in cr:
        if row[column] != firstRowHeader:
            col.append(row[column])

    if savefile is not None: 
        # TODO: Possibly infer file type extension from filename   
        with open(savefile, 'w') as outfile:
            if settings.FILE_EXT == "json":
                json.dump(col, outfile)

    return col

def init_static_data():
    """
    Description
    -----------
    Initializes the three static files defined in app.settings: `STATIC_TICKERS_FILE`, `STATIC_CRYPTO_FILE` and `STATIC_ECON_FILE`. The data for these files is retrieved from the service managers. While this function blurs the lines between file management and service management, the function has been included in the `files.py` module rather than the `services.py` module due the unique response types of static metadata. All metadata is returned a csv or zipped csvs. These responses require specialized functions. Moreover, these files should only be initialized the first time the application executes. Subsequent executions will refer to their cached versions residing in the local or containerized filesytems. 
    """
    if ((not os.path.isfile(settings.STATIC_ECON_FILE)) or \
            (not os.path.isfile(settings.STATIC_TICKERS_FILE)) or \
                (not os.path.isfile(settings.STATIC_CRYPTO_FILE))):

        logger.info('Initializing static data. Please wait. This may take a moment.')
        logger.info('NOTE: set LOG_LEVEL = "debug" for more output while you wait.')
        

        # grab ticker symbols and store in STATIC_DIR
        if not os.path.isfile(settings.STATIC_TICKERS_FILE):
            if settings.PRICE_MANAGER == "alpha_vantage": 

                logger.debug(f'Missing {settings.STATIC_TICKERS_FILE}, querying \'{settings.PRICE_MANAGER}\'')

                # TODO: services calls should be in services.py! need to put this and the helper method 
                #       into services.py in the future. 
                query=f'{settings.PARAM_AV_FUNC}={settings.ARG_AV_FUNC_EQUITY_LISTINGS}'
                url = f'{settings.AV_URL}?{query}&{settings.PARAM_AV_KEY}={settings.AV_KEY}'

                logger.debug(f'Preparsing to parse \'{settings.PRICE_MANAGER}\' Response to query: {query}')
                parse_csv_response_column(column=0, url=url, firstRowHeader=settings.AV_RES_EQUITY_KEY, 
                                                        savefile=settings.STATIC_TICKERS_FILE)

            else:
                logger.info("No PRICE_MANAGER set in .env file!")

        # grab crypto symbols and store in STATIC_DIR
        if not os.path.isfile(settings.STATIC_CRYPTO_FILE):
            if settings.PRICE_MANAGER == "alpha_vantage": 
                logger.debug(f'Missing {settings.STATIC_CRYPTO_FILE}, querying \'{settings.PRICE_MANAGER}\'.')
                url = settings.AV_CRYPTO_LIST

                logger.debug(f'Preparsing to parse \'{settings.PRICE_MANAGER}\' Response to query: {query}')
                parse_csv_response_column(column=0, url=url, firstRowHeader=settings.AV_RES_CRYPTO_KEY, 
                                                    savefile=settings.STATIC_CRYPTO_FILE)
            else:
                logger.info("No PRICE_MANAGER set in .env file!")
            
        # grab econominc indicator symbols and store in STATIC_DIR
        if not os.path.isfile(settings.STATIC_ECON_FILE):
            if settings.STAT_MANAGER == "quandl":
                logger.debug(f'Missing {settings.STATIC_ECON_FILE}, querying \'{settings.STAT_MANAGER}\'.')

                query = f'{settings.PATH_Q_FRED}/{settings.PARAM_Q_METADATA}'
                url = f'{settings.Q_META_URL}/{query}?{settings.PARAM_Q_KEY}={settings.Q_KEY}'

                logger.debug(f'Preparsing to parse \'{settings.PRICE_MANAGER}\' Response to query: {query}')
                parse_csv_response_column(column=0, url=url, firstRowHeader=settings.Q_RES_STAT_KEY,
                                                    savefile=settings.STATIC_ECON_FILE, zipped=settings.Q_RES_STAT_ZIP_KEY)

            else:
                logger.info("No STAT_MANAGER set in .env file!")
    else:
        logger.debug('Static data already initialized!')

def get_static_data(static_type):
    """
    Description
    ----------- 
    Retrieves static data cached in the local or containerized file system. \n \n 

    Parameters
    ----------
    1. `static_type` : str \n
    A string corresponding to the type of static data to be retrieved. The types can be statically accessed through the `app.settings` variables: ASSET_CRYPTO, ASSET_EQUITY and STAT_ECON. \n \n
    """
    logger.debug(f'Loading in cached {static_type} symbols.')
    path = None

    if static_type == settings.ASSET_CRYPTO:
        path = settings.STATIC_CRYPTO_FILE
    
    elif static_type == settings.ASSET_EQUITY:
        path = settings.STATIC_TICKERS_FILE
    
    elif static_type == settings.STAT_ECON:
        path = settings.STATIC_ECON_FILE
    
    else:
        return False

    if path is not None:
        if not os.path.isfile(path):
            init_static_data()

        with open(path, 'r') as infile:
            if settings.FILE_EXT == "json":
                symbols = json.load(infile)   
            # TODO: implement other file loading exts    
        return symbols
        
    return False

def get_watchlist():
    """
    Description
    -----------
    Retrieves the list of watchlisted equity ticker symbols saved in /data/common/watchlist.json.
    """
    logger.debug('Loading in Watchlist symbols.')

    if os.path.isfile(settings.COMMON_WATCHLIST_FILE):
        logger.debug('Watchlist found.')
        with open(settings.COMMON_WATCHLIST_FILE, 'r') as infile:
            if settings.FILE_EXT =="json":
                watchlist = json.load(infile)
                logger.debug('Watchlist loaded in JSON format.')

            # TODO: implement other file loading exts
    else: 
        logger.info('Watchlist not found.')
        watchlist = []

    return watchlist

def add_watchlist(new_tickers):
    """
    Description
    -----------
    Retrieves the list of watchlisted equity ticker symbols saved in /data/common/watchlist.json and then appends to it the list of tickers supplied as arguments. After appending, the list is sorted in alphabetical order. The tickers to add must exist in the /data/static/tickers.json file in order to be added to the watchlist, i.e. the tickers must have price histories that can be retrieved (the static file tickers.json contains a list of all equities with retrievable price histories.) \n \n 
    """
    logger.debug('Saving tickers to Watchlist')

    current_tickers = get_watchlist()
    all_tickers = get_static_data(settings.ASSET_EQUITY)

    for ticker in new_tickers:
        if ticker not in current_tickers and ticker in all_tickers:
            logger.debug(f'New ticker being added to Watchlist: {ticker}')
            current_tickers.append(ticker)

    current_tickers = sorted(current_tickers)

    with open(settings.COMMON_WATCHLIST_FILE, 'w+') as outfile:
        if settings.FILE_EXT == "json":
            json.dump(current_tickers, outfile)
        # TODO: implement other file extensions

def format_allocation(allocation, portfolio, investment=None):
    allocation_format = {}

    if investment is not None:
        shares = portfolio.calculate_approximate_shares(x=allocation, total=investment)
        total = portfolio.calculate_actual_total(x=allocation, total=investment)

    annual_volatility = portfolio.volatility_function(x=allocation) 
    annual_return = portfolio.return_function(x=allocation)

    for j in range(len(portfolio.tickers)):
        allocation_format[j] = {}
        allocation_format[j]['ticker'] = portfolio.tickers[j]
        allocation_format[j]['allocation'] = round(allocation[j], settings.ACCURACY)
        if investment is not None:
            allocation_format[j]['shares'] = float(shares[j])
        allocation_format[j]['annual_return'] = round(portfolio.mean_return[j], settings.ACCURACY) 
        allocation_format[j]['annual_volatility'] = round(portfolio.sample_vol[j], settings.ACCURACY)

    json_format = {}
    json_format['holdings'] = allocation_format

    if investment is not None:
        json_format['total'] = float(total)
        
    json_format['portfolio_return'] = annual_return
    json_format['portfolio_volatility'] = annual_volatility
    
    return json_format

def format_frontier(portfolio, frontier, investment=None):
    json_format = {}
    for i in range(len(frontier)):
        json_format[f'portfolio_{i}'] = format_allocation(allocation=frontier[i], portfolio=portfolio, 
                                                            investment=investment)

    return json_format

def format_moving_averages(tickers, averages_output):
    these_moving_averages, dates = averages_output

    response = {}
    for i in range(len(tickers)):
        ticker_str=f'{tickers[i]}'
        MA_1_str, MA_2_str, MA_3_str = f'{ticker_str}_MA_1', f'{ticker_str}_MA_2', f'{ticker_str}_MA_3'    

        subresponse = {}
        if dates is None:
            subresponse[MA_1_str] = these_moving_averages[i][0]
            subresponse[MA_2_str] = these_moving_averages[i][1]
            subresponse[MA_3_str] = these_moving_averages[i][2]

        else:
            subsubresponse_1, subsubresponse_2, subsubresponse_3 = {}, {}, {}
    
            for j in range(len(dates)):
                date_str=helper.date_to_string(dates[j])
                subsubresponse_1[date_str] = these_moving_averages[i][0][j]
                subsubresponse_2[date_str] = these_moving_averages[i][1][j]
                subsubresponse_3[date_str] = these_moving_averages[i][2][j]

            subresponse[MA_1_str] = subsubresponse_1
            subresponse[MA_2_str] = subsubresponse_2
            subresponse[MA_3_str] = subsubresponse_3

        response[ticker_str] = subresponse
    
    return response

def format_correlation_matrix(tickers, correlation_matrix):
    response = {}
    for i in range(len(tickers)):
        # correlation_matrix[i][i]
        for j in range(i+1, len(tickers)):
            response[f'{tickers[i]}_{tickers[j]}_correlation'] = correlation_matrix[j][i]
    return response
    
def save_allocation(allocation, portfolio, file_name, investment=None):
    save_format = format_allocation(allocation=allocation, portfolio=portfolio, investment=investment)
    save_file(file_to_save=save_format, file_name=file_name)

def save_frontier(portfolio, frontier, file_name, investment=None):
    save_format = format_frontier(portfolio=portfolio, frontier=frontier,investment=investment)
    save_file(file_to_save=save_format, file_name=file_name)

def save_moving_averages(tickers, averages_output, file_name):
    save_format = format_moving_averages(tickers=tickers,averages_output=averages_output)
    save_file(file_to_save=save_format, file_name=file_name)

def save_correlation_matrix(tickers, correlation_matrix, file_name):
    save_format = format_correlation_matrix(tickers=tickers, correlation_matrix=correlation_matrix)
    save_file(file_to_save=save_format, file_name=file_name)
################################################
##### FILE MANAGEMENT FUNCTIONS

# TODO: this deletes subdirectories.
# retain: keeps .gitkeep in directory
def clear_directory(directory, retain=True):
    """
    Description
    -----------
    Wipes a directory of files without deleting the directory itself. \n \n 

    Parameters
    ----------
    1. directory: str \n
    Path of the directory to be cleaned. \n \n 

    2. retain : bool \n
    If set to True, the method will skip files named '.gitkeep' within the directory, i.e. version control configuration files. 

    3. outdated_only: bool \b 
    If set to True, the method will check for a time stamp on files with the format 'DD-MM-YYYY' and retain files that contain this timestamp.
    """
    filelist = list(os.listdir(directory))

    for f in filelist:
        filename = os.path.basename(f)
        if retain and filename == settings.KEEP_EXT:
            continue
        os.remove(os.path.join(directory, f))

def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0