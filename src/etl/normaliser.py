import re

def normalize_year(value):
    value = str(value).strip()
    if value == "TTM":
        return "TTM"
    match = re.match(r"([A-Za-z]{3})\s+(\d{4})",value)
    if match:
        month = match.group(1)
        year = match.group(2)
        month_map = {
            "Jan": "01",
            "Feb": "02",
            "Mar": "03",
            "Apr": "04",
            "May": "05",
            "Jun": "06",
            "Jul": "07",
            "Aug": "08",
            "Sep": "09",
            "Oct": "10",
            "Nov": "11",
            "Dec": "12"
        }
        return f"{year}-{month_map[month]}"
    return None
def normalize_ticker(ticker):
    """ Standardize ticker symbols. """ 
    if ticker is None: 
        return None 
    ticker = str(ticker).strip().upper() 
    ticker = ticker.replace(".NS", "") 
    ticker = ticker.replace(".BO", "") 
    return ticker
