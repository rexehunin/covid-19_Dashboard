from delay_manager import *

def test_current_time_hm():
    assert current_time_hm()
    assert type(current_time_hm()) == str
    time = current_time_hm()
    assert time[2] == ":"
    assert int(time[0:2:]) <= 12
    assert int(time[3:5:]) < 60

def test_delay_calculator():
    assert delay_calculator()
    assert type(delay_calculator()) == int
    assert delay_calculator("00:00")
    assert delay_calculator("23:59")
    delay = delay_calculator()
    assert 0 < delay < 86_400

def test_time_from_midnight():
    assert time_from_midnight("00:00") == 0
    assert time_from_midnight("12:00")
    assert type(time_from_midnight("14:50")) == int
    assert time_from_midnight("15:00") == 54_000

def test_spare_seconds():
    assert spare_seconds()
    assert type(spare_seconds()) == int
    secs = spare_seconds()
    assert 0 <= secs < 60
