from data_fetcher import *

def test_data_collection():
    assert data_collection()
    assert data_collection("Raw")
    assert data_collection("Updates")
    news = data_collection("News")
    assert len(news) == 2
    assert type(data_collection("Covid Data")) == list

def test_data_writing():
    news = data_collection("News")
    assert data_writing("News", news) is None

def test_data_file_config():
    assert data_file_config() is None

