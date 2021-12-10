from config_fetching import *


def test_gather_news_api():
    assert gather_news_api()
    assert type(gather_news_api()) is str
    assert len(gather_news_api()) != 0

def test_gather_page_size():
    assert gather_page_size()
    assert type(gather_page_size()) is int

def test_fetch_location_data():
    assert fetch_location_data()

def test_news_keywords():
    assert news_keywords()
    assert type(news_keywords()) is str
    assert len(news_keywords()) > 0

def test_title():
    assert title()
    assert type(title()) is str
    assert title() is not None
    