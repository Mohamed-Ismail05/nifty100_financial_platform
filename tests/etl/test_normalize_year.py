from src.etl.normaliser import normalize_year
print(normalize_year("FY24"))
def test_year_01(): 
    assert normalize_year("FY24") == 2024 
def test_year_02(): 
    assert normalize_year("FY2024") == 2024 
def test_year_03(): 
    assert normalize_year("2024") == 2024 
def test_year_04(): 
    assert normalize_year("2024.0") == 2024 
def test_year_05(): 
    assert normalize_year("2023-24") == 2024 
def test_year_06(): 
    assert normalize_year("FY23") == 2023 
def test_year_07(): 
    assert normalize_year("FY2023") == 2023 
def test_year_08(): 
    assert normalize_year("2022") == 2022 
def test_year_09(): 
    assert normalize_year("FY22") == 2022 
def test_year_10(): 
    assert normalize_year("2021-22") == 2022 
def test_year_11():
    assert normalize_year(" FY24 ") == 2024 
def test_year_12(): 
    assert normalize_year("FY25") == 2025 
def test_year_13(): 
    assert normalize_year("FY2025") == 2025 
def test_year_14(): 
    assert normalize_year("2025") == 2025 
def test_year_15(): 
    assert normalize_year("FY26") == 2026 
def test_year_16(): 
    assert normalize_year("2026") == 2026 
def test_year_17(): 
    assert normalize_year("2020-21") == 2021 
def test_year_18(): 
    assert normalize_year("FY21") == 2021 
def test_year_19(): 
    assert normalize_year(None) is None 
def test_year_20(): 
    assert normalize_year("invalid") is None