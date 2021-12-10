"""[This module is the core of the Covid-19 Dashboard software. Running this module will
initialise and run the dashboard at 127.0.0.1]"""
# Imports

import time
import sched
import logging
from flask import Flask, render_template, redirect, url_for, request
from covid_data_handler import (covid_api_data_refiner, covid_API_request, remove_update,
schedule_covid_updates, update_adder)
from covid_news_handling import update_news, news_remover
from config_fetching import fetch_location_data, title
from data_fetcher import data_collection, data_file_config, data_writing
from delay_manager import delay_calculator, time_from_midnight


app = Flask(__name__)
schedule = sched.scheduler(time.time, time.sleep)

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s:%(funcName)s:%(levelname)s:%(message)s")
file_handler = logging.FileHandler('program_log.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Functions

@app.route('/')
def home_screen_initialise():
    """[This function sets up the data and data structures needed to operate the program. Should
    only be called once, upon initial run of the code]

    Returns:
        [Flask template]: [Returns a flask template to the web browser, containing all data to be
        displayed to the user]
    """
    logger.info("Initialised Webpage")
    location, nation = fetch_location_data()
    updates = []
    covid_data=()
    if location == "Exeter":
        covid_data=covid_api_data_refiner(covid_API_request(), covid_API_request(nation, "nation"))
    else:
        covid_data=covid_api_data_refiner(covid_API_request(location),
        covid_API_request(nation, "nation"))

    # location, local_cases_seven_days, nation, national_cases_seven_days
    # cum_daily_deaths, hospital_cases
    data_file_config()
    update_news()
    news = data_collection("News")
    data_writing("Covid Data", covid_data)

    return render_template('index.html', title=title(), location = location,
    local_7day_infections = covid_data[1], nation_location = nation,
    national_7day_infections = covid_data[3], hospital_cases = covid_data[4],
    deaths_total = covid_data[5], news_articles = news[0], updates = updates,
    image = "safe_image.png")


@app.route('/index/')
def home_screen():
    """[The home screen of the program deals with any and all user interaction with the webpage]

    Returns:
        [Flask template]: [Function returns a flask outline to the webpage, containing all data to
        be displayed to the user]
    """
    global schedule
    # Carries the schedule into the function so that it may be added to/have items removed
    covid_data = data_collection("Covid Data")
    logger.info(covid_data)
    try:
        assert covid_data[4] # Checks to see if the data has been initialised in previous function
    except IndexError:
        return redirect(url_for("home_screen_initialise"))
        # Return to intialise program before returning to this function

    # Gathering the variables from a scheduling request
    logger.info(schedule.queue)
    alarm_name = request.args.get('two')
    news_remove = request.args.get('notif')
    update_remove = request.args.get('update_item')
    if alarm_name: # Returns true if two has any value (an update request MUST have a two value)
        alarm_time = request.args.get('update')
        repeat = request.args.get('repeat')
        covid_update = request.args.get('covid-data')
        news_update = request.args.get('news')
        update_info = ""
        logger.info("All variables collected from browser")
        if alarm_time:
            update_info += "Time: " + alarm_time + "    "
        update_info += "Covid Data Update:"
        delay = delay_calculator(alarm_time)
        if covid_update: # All data is priority 0
            update_info += " ✔ "
            if repeat:
                schedule.enter(delay, 0, schedule_covid_updates, ("", 0, True, schedule,))
                # Update covid data such that it repeats
            else:
                schedule.enter(delay, 0, schedule_covid_updates, ("", 0,))
                # Update covid data such that it does not repeat
        else:
            update_info += " ❌ "
        update_info += " Covid News Update:"
        if news_update: # All news is priority 1
            update_info += " ✔ "
            if repeat:
                schedule.enter(delay, 1, update_news, (True, schedule,))
                # Update news articles such that it repeats
            else:
                schedule.enter(delay, 1, update_news)
                # Update news articles once
        else:
            update_info += " ❌ "
        if repeat:
            update_info += " Repeating: ✔"
        else:
            update_info += " Repeating: ❌"

        update_adder({"title": alarm_name, "content": update_info,
        "time": time_from_midnight(alarm_time)})
    if news_remove:
        news_remover(news_remove)
        # remove news item

    if update_remove:
        remove_update(update_remove, schedule)
        # remove a scheduled update (both from the list and the schedule itself)

    news, covid_data, updates = data_collection()
    schedule.run(blocking=False)
    return render_template('index.html', title=title(), location=covid_data[0],
    local_7day_infections=covid_data[1], nation_location=covid_data[2],
    national_7day_infections=covid_data[3], hospital_cases=covid_data[4],
    deaths_total=covid_data[5], news_articles=news[0], updates=updates, image="safe_image.png")



# Main

if __name__ == "__main__":
    schedule.run(blocking=False)
    app.run()
