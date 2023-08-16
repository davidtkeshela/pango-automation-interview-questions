import pytest
import requests
from automation_framework.utilities.api_helpers import ApiHelper
from automation_framework.utilities.Enums import TempUnits
from automation_framework.utilities.db_helpers import DatabaseHelper

@pytest.fixture(scope="module")
def api():
    return ApiHelper()

@pytest.mark.parametrize("city", [
    "Tbilisi",
    "New York",
    "Los Angeles",
    "London"
])
def test_get_weather_data(api, city):
    response = api.get_current_weather(city, "en", TempUnits.Unit.CELSIUS.description)

    assert response.status_code == 200

    responseJson = response.json()
    temperature = responseJson["main"]["temp"]
    feelsLike = responseJson["main"]["feels_like"]

    dbHelper = DatabaseHelper()
    weather_data = dbHelper.get_weather_data(city)

    if weather_data:
        temperature_db, feels_like_db = weather_data
        if temperature_db != temperature and feels_like_db != feelsLike:
            dbHelper.insert_weather_data(city, temperature, feelsLike)
            new_weather_data = dbHelper.get_weather_data(city)
            if new_weather_data:
                new_temperature_db, new_feels_like_db = new_weather_data
                assert new_temperature_db == temperature
                assert new_feels_like_db == feelsLike
    else:
        print(f"No data found for {city}.")