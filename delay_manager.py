"""[This module contains functions to do with time and delay, in relation to the schedule utilised
    in the main module]"""
# Imports

import time
import logging

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s:%(funcName)s:%(levelname)s:%(message)s")
file_handler = logging.FileHandler('program_log.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Functions

def current_time_hm() -> str:
    """[Returns the current time for reference/manipulation]

    Returns:
        str: [Current time, formatted as hh:mm]
    """
    current_time = time.gmtime()
    current_hour = current_time[3]
    current_minute = current_time[4] + 1
    formatted_time = str(current_hour) + ":" + str(current_minute)
    return formatted_time

def delay_calculator(update_time: str = current_time_hm()) -> int:
    """[Calculates the required delay to correctly schedule events]

    Args:
        update_time (str, optional): [The time when the event needs to occur].
        Defaults to current_time_hm().

    Returns:
        int: [The time, in seconds, until the event needs to be executed]
    """
    update_hour = int(update_time[0:2:])
    update_minute = int(update_time[3:5:])
    current_time = time.gmtime()
    update_hour_bigger = update_hour > current_time[3]
    update_minute_bigger = (update_hour == current_time[3]) and (update_minute >= current_time[4])
    if update_hour_bigger or update_minute_bigger:
        hour_dif = (update_hour-current_time[3])*(60*60)
        seconds_dif=hour_dif+(update_minute-current_time[4])*60-current_time[5]
        logger.info("This event will occur later today, in %s seconds", str(seconds_dif))
    else:
        hour_dif = (current_time[3] - update_hour) * (60*60)
        minute_dif = (current_time[4] - update_minute) * 60
        seconds_dif = (24*60*60) - (hour_dif + minute_dif - current_time[5])
        logger.info("This event will occur tomorrow, in %s seconds", str(seconds_dif))
    return seconds_dif

def time_from_midnight(update_time: str) -> int:
    """[The time from midnight to the specified time passed to the function, used to repeat events
    effectively]

    Args:
        update_time (str): [The time the event is scheduled]

    Returns:
        int: [The number of seconds it would take from midnight to reach the time specified in
        update_time]
    """
    update_hour = int(update_time[0:2:])
    update_minute = int(update_time[3:5:])

    seconds = ((update_hour*(60*60)) + (update_minute*(60)))
    return seconds

def spare_seconds() -> int:
    """[Specifies the number of excess seconds to ensure repeated events are placed on the minute]

    Returns:
        int: [The number of seconds over the time when the page has updated, allowing the function
        to repeat accurately (not progressively getting later)]
    """
    current_time = time.gmtime()
    return current_time[5]
