"""[This module contains functions for fetching data from the data.json file]"""
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

def data_collection(data_field:str = "All") -> list:
    """[Collects the specified key from the data.json dictionary]

    Args:
        data_field (str, optional): [The key of the data that needs to be fetched. "All" will
        return 3 separate lists found within the json file. "Raw" simply returns the
        contents of the file without alteration]. Defaults to "All".

    Returns:
        list: [Returns either a single list specified by the data_field attribute or a
        tuple of all 3 dictionaries for quick assignment of the data]
    """
    with open("data.json", "r", encoding="UTF-8") as data:
        all_data = json.load(data)
    if data_field == "All":
        return_data = (all_data["News"], all_data["Covid Data"], all_data["Updates"])
    elif data_field == "Raw":
        return_data = all_data
    else:
        return_data = all_data[data_field]
    return return_data

def data_writing(data_field:str, new_data:list) -> None:
    """[Writes the given data to the specified array/list in the data.json file]

    Args:
        data_field (str): [The key of the dictionary for the data to be saved in]
        new_data (list): [The data to be saved]
    """
    all_data = data_collection("Raw")
    all_data[data_field] = new_data
    try:
        with open("data.json", "w", encoding="UTF-8") as file:
            json.dump(all_data,file)
            file.close()
    except PermissionError:
        logger.critical("Permission not granted to access data.json// DATA NOT WRITTEN //")

def data_file_config() -> None:
    """[Sets/Resets the data.json file when the home_screen is initialised]
    """
    file_format = {
        "News": [[],[]],
        "Covid Data": [],
        "Updates": []
    }
    with open("data.json", "w", encoding="UTF-8") as data_config_file:
        json.dump(file_format, data_config_file)
        data_config_file.close()
