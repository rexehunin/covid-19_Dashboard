"""[Functions that facilitate the fetching of data from the congif file]"""
# Imports

import json
import logging

# Logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s:%(funcName)s:%(levelname)s:%(message)s")
file_handler = logging.FileHandler('program_log.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Functions

def gather_news_api() -> str:
    """[Returns the News API from the config file]

    Returns:
        str: [The News API]
    """
    with open("config.json", "r", encoding="UTF-8") as config:
        config_data = json.load(config)
        credentials = config_data["Credentials"]
        news_api = credentials["News_API"]
    if news_api == "":
        logging.fatal("No news API key in config file")
        raise ValueError("No news API key in config file")
    logger.info("Gathered News API")
    return news_api

def gather_page_size() -> int:
    """[Returns the desired page size of the API request from the config file]

    Returns:
        int: [The number of news articles fetched every time a news API request is made]
    """
    try:
        with open("config.json", encoding="UTF-8") as config:
            config_data = json.load(config)
            page_size = config_data["Variable Data"]["Number of news articles"]
        logger.info("Gathered desired page size")
    except KeyError:
        page_size = 10
        logger.error("Desired page number couldn't be found, default utilised")
    return page_size

def fetch_location_data() -> tuple:
    """[Fetches the ltla and nation data saved in the config file]

    Returns:
        tuple: [(ltla, nation) The desired low tier local authority and nation which the data is
        related to]
    """
    with open("config.json", encoding="UTF-8") as config:
        config_data=json.load(config)
        ltla = (config_data["Variable Data"])["ltla"]
        nation = (config_data["Variable Data"])["nation"]
    logger.info("Gathered ltla and nation name")
    return(ltla, nation)

def news_keywords() -> str:
    """[Fetches the keywords used to gather news articles]

    Returns:
        str: [A string of the keywords searched for by the news API]
    """
    with open("config.json", encoding="UTF-8") as config:
        config_data = json.load(config)
        news_kw = config_data["Variable Data"]["News Key Terms"]
    logger.info("Gathered news keywords from config")
    return news_kw


def title() -> str:
    """[Returns the title for the Dashboard]

    Returns:
        str: [The title of the dashboard as outlined in the config file]
    """
    with open("config.json", encoding="UTF-8") as config:
        config_data = json.load(config)
        title_string = config_data["Variable Data"]["Title"]
    logger.info("Gathered title from config")
    return title_string
