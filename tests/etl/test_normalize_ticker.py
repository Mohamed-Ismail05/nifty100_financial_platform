from src.etl.normaliser import normalize_ticker 

def test_ticker_01(): 
    assert normalize_ticker("tcs") == "TCS" 
def test_ticker_02(): 
    assert normalize_ticker("TCS") == "TCS" 
def test_ticker_03(): 
    assert normalize_ticker("TCS.NS") == "TCS" 
def test_ticker_04(): 
    assert normalize_ticker("TCS.BO") == "TCS" 
def test_ticker_05(): 
    assert normalize_ticker(" tcs ") == "TCS" 
def test_ticker_06(): 
    assert normalize_ticker("infy") == "INFY" 
def test_ticker_07(): 
    assert normalize_ticker("INFY.NS") == "INFY" 
def test_ticker_08(): 
    assert normalize_ticker("INFY.BO") == "INFY" 
def test_ticker_09(): 
    assert normalize_ticker("reliance") == "RELIANCE" 
def test_ticker_10(): 
    assert normalize_ticker("RELIANCE.NS") == "RELIANCE" 
def test_ticker_11(): 
    assert normalize_ticker("hdfcbank") == "HDFCBANK" 
def test_ticker_12(): 
    assert normalize_ticker("HDFCBANK.NS") == "HDFCBANK" 
def test_ticker_13(): 
    assert normalize_ticker("icicibank") == "ICICIBANK" 
def test_ticker_14(): 
    assert normalize_ticker("ICICIBANK.BO") == "ICICIBANK" 
def test_ticker_15(): 
    assert normalize_ticker("sbin") == "SBIN" 
def test_ticker_16(): 
    assert normalize_ticker("SBIN.NS") == "SBIN" 
def test_ticker_17(): 
    assert normalize_ticker("asianpaint") == "ASIANPAINT" 
def test_ticker_18(): 
    assert normalize_ticker("ASIANPAINT.BO") == "ASIANPAINT" 
def test_ticker_19(): 
    assert normalize_ticker(None) is None 
def test_ticker_20(): 
    assert normalize_ticker(" wipro ") == "WIPRO"