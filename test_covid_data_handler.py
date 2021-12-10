from covid_data_handler import *

def test_parse_csv_data():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639

def test_process_covid_csv_data():
    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data ( parse_csv_data (
            'nation_2021-10-28.csv' ) )
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544

def test_covid_api_request():
    data = covid_API_request()
    assert isinstance(data, dict)
    assert covid_API_request("England", "nation")
    assert covid_API_request("East Devon")
    assert "newCasesBySpecimenDate" in data.keys()

def test_covid_api_data_refiner():
    data = covid_api_data_refiner(covid_API_request(), covid_API_request("England", "nation"))
    assert covid_api_data_refiner(covid_API_request(), covid_API_request("England", "nation"))
    assert data[0] == "Exeter"
    assert type(data[1]) is int
    assert len(data) == 6

def test_schedule_covid_updates():
    schedule_covid_updates(update_interval=10, update_name='update test')
    assert schedule_covid_updates("Update", 1000) is None
    assert schedule_covid_updates("Update Now") is None