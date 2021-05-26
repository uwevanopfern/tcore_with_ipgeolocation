import requests
import json
import dateutil.parser
from requests.adapters import HTTPAdapter
from django.contrib.auth.models import User
from .models import Location, Holiday
from requests.packages.urllib3.util.retry import Retry


def requests_retry_session(
    retries=10,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 503, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def abstract_api_email_validate(email):

    params = {"api_key": "e28c4b0d191b4ddb817f88c694aee489", "email": email}
    response = requests_retry_session().get(
        "https://emailvalidation.abstractapi.com/v1/", params=params
    )

    parsed = json.loads(response.content)
    deliverability = parsed["deliverability"]

    if deliverability == "DELIVERABLE":
        return True
    return False


def abstract_api_get_ipgeolocation(user):
    params = {"api_key": "c5c241b9c27d4386bcb653124866d13e"}
    response = requests_retry_session().get(
        "https://ipgeolocation.abstractapi.com/v1/", params=params
    )

    user = User.objects.get(username=user)

    parsed = json.loads(response.content)

    ip_address = parsed["ip_address"]
    city = parsed["city"]
    region = parsed["region"]
    region_iso_code = parsed["region_iso_code"]
    postal_code = parsed["postal_code"]
    country = parsed["country"]
    country_code = parsed["country_code"]
    country_is_eu = parsed["country_is_eu"]
    continent = parsed["continent"]
    continent_code = parsed["continent_code"]
    currency_name = parsed["currency"]["currency_name"]
    currency_code = parsed["currency"]["currency_code"]

    Location(
        user=user,
        ip_address=ip_address,
        city=city,
        region=region,
        region_iso_code=region_iso_code,
        postal_code=postal_code,
        country=country,
        country_code=country_code,
        country_is_eu=country_is_eu,
        continent=continent,
        continent_code=continent,
        currency_name=currency_name,
        currency_code=currency_code,
    )

    # Convert timezone date_joined date to the current date format of holidays API (05/23/2021)
    user_date_joined = user.date_joined
    d = dateutil.parser.parse(str(user_date_joined))
    fmt = "%m/%d/%Y"
    converted_date_joined = d.strftime(fmt)

    arr_date = converted_date_joined.split("/")
    month = arr_date[0]
    day = arr_date[1]
    year = arr_date[2]

    # check if date_joined of a newely created user has the same holiday of user country
    params = {
        "api_key": "595f5c769b264ba68477475ceb87a7e3",
        "country": country_code,
        "year": year,
        "month": month,
        "day": day,
    }

    holidays_response = requests_retry_session().get(
        "https://holidays.abstractapi.com/v1/", params=params
    )

    parsed_holidays_data = json.loads(holidays_response.content)

    if parsed_holidays_data:
        # loop through array and save each instance in database
        for holiday in parsed_holidays_data:
            name = holiday["name"]
            name_local = holiday["name_local"]
            country = holiday["country"]
            location = holiday["location"]
            type = holiday["type"]
            date = holiday["date"]
            week_day = holiday["week_day"]

            Holiday(
                user=user,
                country=country,
                name=name,
                name_local=name_local,
                location=location,
                type=type,
                date=date,
                week_day=week_day,
            )
            return
    return
