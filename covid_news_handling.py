"""[This module contains all functions that involve news adding, gathering or manipulation]"""
# Imports

import sched
import time
import logging
import requests

from config_fetching import news_keywords, gather_news_api, gather_page_size
from data_fetcher import data_collection, data_writing
from delay_manager import spare_seconds

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s:%(funcName)s:%(levelname)s:%(message)s")
file_handler = logging.FileHandler('program_log.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Functions

def news_API_request(covid_terms:str = news_keywords(), today_only:bool = False) -> list:
    """[Gathers news using newsapi.org to fetch relevant articles]

    Args:
        covid_terms (str, optional): [The terms used to search for articles]. Defaults to
        news_keywords().
        today_only (bool, optional): [Specifies if the articles fetched are from today only].
        Defaults to False.

    Returns:
        list: [A list of dictionaries containing news articles for the interface]
    """
    todays_date = time.gmtime()
    date_y_m_d = (str(todays_date[0])+"-"+str(todays_date[1])+"-"+str(todays_date[2]))

    news_api = gather_news_api()
    page_size = gather_page_size()

    url = ("https://newsapi.org/v2/everything?")
    url += "q=" + covid_terms
    url += "&sources=bbc-news,google-news-uk" # ,independent"
    url += "&language=en"
    url += "&sortBy=publishedAt"
    url += "&pageSize=" + str(page_size)
    url += "&apiKey=" + news_api

    if today_only is True:
        url += "&from" + date_y_m_d
        logger.info("Only articles published today fetched")
    response = requests.get(url)
    news = response.json()

    # if news["status"] != "ok":
    try:
        logger.info("News Gathered")
        for i in range(0, len(news["articles"])):
            content = news["articles"][i]["content"]
            for j in range(0, len(content) - 2):
                if content[j] == "…":
                    news["articles"][i]["content"] = content[0:j+1:]
                    news["articles"][i]["content"] += " \nSource: " + news["articles"][i]["url"]
                    break
    except:
        logger.error("News unable to be gathered")
        news = {
            "articles":[]
        }
    return news["articles"]

def update_news(repeat:bool = False, schedule:sched = None) -> None:
    """[Updates the news located in the data.json file]

    Args:
        repeat (bool, optional): [Specifies if the scheduled action is repeated].
        Defaults to False.
        schedule (sched, optional): [The schedule to add the repeated event to].
        Defaults to None.
    """
    news = data_collection("News")

    fresh_articles = news_API_request()
    for i in range(0, len(fresh_articles)):
        if (fresh_articles[i])["publishedAt"] in news[1]:
            break
        elif fresh_articles[i] in news[0]:
            break
        else:
            news[0].insert(i, fresh_articles[i])
    try:
        if repeat:
            schedule.enter(86400 - spare_seconds(), 1, update_news, (True, schedule,))
    except AttributeError:
        logger.error("Attempted to pass data to schedule without passing schedule to function")
        logger.debug("Update cancelled")

    data_writing("News", news)



def news_remover(title:str) -> None:
    """[Removes specified news article from the news array]

    Args:
        title (str): [The title of the news article to be removed]
    """
    news = data_collection("News")
    news_article_found = False
    for i in range(0, len(news[0])):
        if news[0][i]["title"] == title:
            removed_article = news[0].pop(i)
            news_article_found = True
            break
    logger.info("%s . Article removed", title)
    if news_article_found is True:
        news[1].append(removed_article["publishedAt"])
    data_writing("News", news)
