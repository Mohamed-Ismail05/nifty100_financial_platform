from src.etl.normaliser import normalize_year
def test_year_01():
    assert normalize_year("Mar 2024") == "2024-03"
def test_year_02():
    assert normalize_year("Mar 2023") == "2023-03"
def test_year_03():
    assert normalize_year("Mar 2022") == "2022-03"
def test_year_04():
    assert normalize_year("Mar 2021") == "2021-03"
def test_year_05():
    assert normalize_year("Dec 2020") == "2020-12"
def test_year_06():
    assert normalize_year("Dec 2019") == "2019-12"
def test_year_07():
    assert normalize_year("Jan 2018") == "2018-01"
def test_year_08():
    assert normalize_year("Feb 2017") == "2017-02"
def test_year_09():
    assert normalize_year("Apr 2016") == "2016-04"
def test_year_10():
    assert normalize_year("May 2015") == "2015-05"
def test_year_11():
    assert normalize_year("Jun 2014") == "2014-06"
def test_year_12():
    assert normalize_year("Jul 2013") == "2013-07"
def test_year_13():
    assert normalize_year("Aug 2012") == "2012-08"
def test_year_14():
    assert normalize_year("Sep 2011") == "2011-09"
def test_year_15():
    assert normalize_year("Oct 2010") == "2010-10"
def test_year_16():
    assert normalize_year("Nov 2009") == "2009-11"
def test_year_17():
    assert normalize_year("TTM") == "TTM"
def test_year_18():
    assert normalize_year(" Mar 2024 ") == "2024-03"
def test_year_19():
    assert normalize_year("Invalid") is None
def test_year_20():
    assert normalize_year("") is None