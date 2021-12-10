from covid_news_handling import *

def test_news_API_request():
    assert news_API_request()
    assert type(news_API_request) == list
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus', True)
    assert news_API_request('Football Goal League')

def test_update_news():
    assert update_news() is None
    assert update_news(True)

