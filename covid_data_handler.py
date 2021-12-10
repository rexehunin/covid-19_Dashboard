"""[Contains all functions pertinent to the Covid-19 data to be displayed on the webpage]"""
# Imports

import sched # Module used to schedule events
import logging # Module used to log the activities of the code
from uk_covid19 import Cov19API # An API that allows for collection of UK Coronavirus data
from config_fetching import fetch_location_data
from data_fetcher import data_collection, data_writing
from delay_manager import spare_seconds

# Functions

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s:%(funcName)s:%(levelname)s:%(message)s")
file_handler = logging.FileHandler('program_log.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def parse_csv_data(csv_filename:str) -> list:
    """[Reads the lines of the specified CSV file and returns the stored data]

    Args:
        csv_filename (str): [The name of the file which needs to be parsed]

    Returns:
        list: [A list of the lines within the CSV file]
    """
    with open(csv_filename, "r", encoding="UTF-8") as csv_content:
        csv_lines = csv_content.readlines()
    logger.info("Gathered data from the CSV file")
    return csv_lines


def process_covid_csv_data(covid_csv_data: list) -> tuple:
    """[Takes the lines of data from the CSV file and refines the data into the desired outputs]

    Args:
        covid_csv_data (list): [A list of lines from the CSV file]

    Returns:
        tuple: [Returns the total number of cases in the last 7 days, the current number of
        hospital cases and the cumulative number of deaths]
    """

    index = 0
    refined_covid_csv_data = []
    for i in range(0, 30): # Gathers the first 30 elements of the data (last month)
        refined_covid_csv_data.append([]) # Adds empty array to represent data from 1 day
        covid_csv_data[i] = covid_csv_data[i].strip("\n") # Removes the special character \n
        index = 0
        for j in range(0, len(covid_csv_data[i])):
            if (covid_csv_data[i])[j] == ",": # Separates data by the commas
                new_data= (covid_csv_data[i])[index:j:]
                refined_covid_csv_data[i].append(new_data)
                index = j + 1
        new_data = (covid_csv_data[i])[index::]
        refined_covid_csv_data[i].append(new_data) # Adds the new data to the refined data list

    # Evaluates the cumulative number of deaths from the data

    cumulative_deaths_index = None
    for i in range(0, len(refined_covid_csv_data[0])):
        if refined_covid_csv_data[0][i] == "cumDailyNsoDeathsByDeathDate":
            cumulative_deaths_index = i
            break

    if cumulative_deaths_index is None:
        cumulative_deaths = None
    else:
        for i in range(1, len(refined_covid_csv_data)):
            if refined_covid_csv_data[i][cumulative_deaths_index]:
                cumulative_deaths = int(refined_covid_csv_data[i][cumulative_deaths_index])
                break

    # Cases in the last 7 days
    # Ignore the most recent data entry, as it is incomplete

    covid_cases_index = None
    for i in range(0, len(refined_covid_csv_data[0])):
        if refined_covid_csv_data[0][i] == "newCasesBySpecimenDate":
            covid_cases_index = i
            break

    if covid_cases_index is None:
        cases_seven_days = None
    else:
        cases_seven_days = 0
        skip_first = False
        for i in range(0, len(refined_covid_csv_data)):
            if refined_covid_csv_data[i][covid_cases_index].isdigit():
                if skip_first is False:
                    skip_first = True
                else:
                    for j in range(i, i+7):
                        cases_seven_days += int(refined_covid_csv_data[j][covid_cases_index])
                    break

    # Hospital cases
    hospital_cases_index = None
    for i in range(0, len(refined_covid_csv_data[0])):
        if refined_covid_csv_data[0][i] == "hospitalCases":
            hospital_cases_index = i
            break

    if hospital_cases_index is None:
        hospital_cases = None
    else:
        for i in range(0, len(refined_covid_csv_data)):
            if refined_covid_csv_data[i][hospital_cases_index].isdigit():
                hospital_cases = int(refined_covid_csv_data[i][hospital_cases_index])
                break

    return(cases_seven_days, hospital_cases, cumulative_deaths)

def covid_API_request(location:str = "Exeter", location_type:str = "ltla") -> dict:
    """[Collects up to date data from the uk_covid19 module]

    Args:
        location (str, optional): [The name of the location the data will be relevant to].
        Defaults to "Exeter".
        location_type (str, optional): [The type of location specified before]. Defaults to "ltla".

    Returns:
        dict: [A dictionary of all data relevant to the location passed]
    """
    location_filter = []
    location_filter.append("areaType=" + location_type)
    location_filter.append("areaName=" + location)

    if location_type != "nation":
        covid_data_structure = {
            "date": "date",
            "areaName": "areaName",
            "newCasesBySpecimenDate": "newCasesBySpecimenDate"
        }
    else:
        covid_data_structure = {
            "date": "date",
            "areaName": "areaName",
            "newCasesBySpecimenDate": "newCasesBySpecimenDate",
            "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",
            "hospitalCases": "hospitalCases"
        }

    api = Cov19API(filters = location_filter, structure = covid_data_structure)
    data = api.get_json()

    return data["data"]


def covid_api_data_refiner(local_covid_api_data: dict, national_covid_api_data: dict) -> tuple:
    """[Takes the local and national data as returned by covid_api_request() and outputs the
    desired values from that data]

    Args:
        local_covid_api_data (dict): [Covid data from the desired low tier local authority]
        national_covid_api_data (dict): [Covid data from the associated nation of the low tier
        local authority]

    Returns:
        tuple: [A tuple containing the ltla, local cases from the past 7 days, nation, national
        cases from the past 7 days, cumulative national deaths and current hospital cases
        nationally]
    """

    # location
    location = local_covid_api_data[0]["areaName"]

    # local_7day_infections
    local_cases_seven_days = 0
    skip_first = False
    for i in range(0, len(local_covid_api_data)):
        if local_covid_api_data[i]["newCasesBySpecimenDate"] is not None:
            if skip_first is False:
                skip_first = True
            else:
                for j in range(i, i+7):
                    local_cases_seven_days += local_covid_api_data[j]["newCasesBySpecimenDate"]
                break

    # Nation
    nation = (national_covid_api_data[0])["areaName"]

    # National cases

    national_cases_seven_days = 0
    skip_first = False
    for i in range(0, len(national_covid_api_data)):
        if national_covid_api_data[i]["newCasesBySpecimenDate"] is not None:
            if skip_first is False:
                skip_first = True
            else:
                for j in range(i, i+7):
                    national_cases_seven_days+=national_covid_api_data[j]["newCasesBySpecimenDate"]
                break


    # National Cumulative Deaths

    for i in range(0, len(national_covid_api_data)):
        if national_covid_api_data[i]["cumDailyNsoDeathsByDeathDate"] is not None:
            cum_daily_deaths = national_covid_api_data[i]["cumDailyNsoDeathsByDeathDate"]
            break
    cum_daily_deaths = "National Deaths: " + str(cum_daily_deaths)
    # National hospital cases

    for i in range(0, len(national_covid_api_data)):
        if national_covid_api_data[i]["hospitalCases"] is not None:
            hospital_cases = national_covid_api_data[i]["hospitalCases"]
            break
    hospital_cases = "Hospital Cases: " + str(hospital_cases)

    return(location, local_cases_seven_days, nation, national_cases_seven_days,
    cum_daily_deaths, hospital_cases)


def update_adder(update: dict) -> None:
    """[Adds the specified update to the update array]

    Args:
        update (dict): [A dictionary specifying details to the update being added]
    """
    current_updates = data_collection("Updates")
    if update not in current_updates:
        current_updates.append(update)
        data_writing("Updates", current_updates)
        logger.info("Update added to the update array")


def schedule_covid_updates(update_name:str, update_interval:int=0, repeat:bool=False,
schedule:sched=None) -> None:
    """[Refreshes the covid data held in the data.json file]

    Args:
        update_name (str): [The name given for the update]
        update_interval (int, optional): [The interval of the update]. Defaults to 0.
        repeat (bool, optional): [Specifies if scheduled update is repeated]. Defaults to False.
        schedule (sched, optional): [The schedule to renew a repeated event]. Defaults to None.
    """
    ltla, nation = fetch_location_data()
    if ltla == "Exeter":
        covid_data = covid_api_data_refiner(covid_API_request(),
        covid_API_request(nation, "nation"))
        # location, local_cases_seven_days, nation, national_cases_seven_days,
        # cumDailyDeaths, hospital_cases
    else:
        covid_data = covid_api_data_refiner(covid_API_request(ltla),
        covid_API_request(nation, "nation"))
        # location, local_cases_seven_days, nation, national_cases_seven_days,
        # cum_daily_deaths, hospital_cases

    try:
        if repeat:
            schedule.enter(86400 - spare_seconds(), 0, schedule_covid_updates,
            ("", 0, True, schedule))
    except AttributeError:
        logger.error("Attempted to pass data to schedule without passing schedule to function")
        logger.info("Update cancelled")

        remove_update(update_name)
    data_writing("Covid Data", covid_data)

def remove_update(update_name:str, schedule:sched = None) -> None:
    """[Removes an update from both the update array and the schedule]

    Args:
        update_name (str): [The name of the update to be removed]
        schedule (sched, optional): [The schedule from which to remove the event].
        Defaults to None.
    """
    logger.debug("Reached function")
    updates = data_collection("Updates")
    update_times = []
    remove_indexes = []
    for i in range(0, len(updates)):
        if updates[i]["title"] == update_name:
            update_times.append(updates[i]["time"])
            remove_indexes.append(i)
    logger.debug(update_times)

    if schedule is not None:
        events = schedule.queue
        logger.debug(events)
        logger.debug(remove_indexes)
        for i in range(len(events)- 1, -1 , -1):
            if int(events[i][0]) % (60*60*24) in update_times:
                schedule.cancel(events[i])
    else:
        logger.debug("Schedule not provided for function. Assume event not in schedule")

    for i in range(len(remove_indexes)-1 , -1, -1):
        updates.pop(i)
    logger.debug(updates)
    data_writing("Updates", updates)
