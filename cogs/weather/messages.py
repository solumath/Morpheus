from config.messages import GlobalMessages


class WeatherMess(GlobalMessages):
    weather_brief = "Get weather status of specific place"
    place_not_found = "I could not find a place `{place}` with that name"
    token_error = "The used token is invalid"
    weather_error = "The api returned error\n{error}"
    invalid_place_format = "Invalid place format `{place}`"
    website_unreachable = "[The Weather website](http://api.openweathermap.org) is unreachable"
