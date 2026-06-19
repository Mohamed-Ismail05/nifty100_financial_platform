""" Utility functions for standardizing financial datasets. """
import re 
def normalize_year(year_value):
    """ Convert year values into a standard YYYY format. """
    if year_value is None:
        return None 
    year_value = str(year_value).strip() 
    match = re.search(r"(20\d{2})-(\d{2})$", year_value)
    if match:
        return int("20" + match.group(2))
    match = re.search(r"(20\d{2})", year_value) 
    if match: 
        return int(match.group(1)) 
    match = re.search(r"(\d{2})$", year_value)
    if match:
            return int("20" + match.group(1)) 
    return None 
def normalize_ticker(ticker):
    """ Standardize ticker symbols. """ 
    if ticker is None: 
        return None 
    ticker = str(ticker).strip().upper() 
    ticker = ticker.replace(".NS", "") 
    ticker = ticker.replace(".BO", "") 
    return ticker
