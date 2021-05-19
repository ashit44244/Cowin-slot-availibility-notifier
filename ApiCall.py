import requests
import json
from telegram_bot_rest_call_bot import telegram_bot_sendtext
from datetime import datetime


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}

systemDate = datetime.today().strftime('%d-%m-%Y')
district_id = 294  # 294- BBMP
age= 32
result = []

getStatesListUrl = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
calendarByDistrictUrl = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict"

queryparam = {'district_id': district_id, 'date': systemDate}

response = requests.get(calendarByDistrictUrl,
                        headers=headers, params=queryparam)
print(response)
# print(response.json())
if response.ok:
    resp_json = response.json()
    # print(json.dumps(resp_json, indent = 1))
    if resp_json["centers"]:
        print("Available on: ", systemDate, "for 18-45 age group ,user age: ",age)
        for center in resp_json["centers"]:
            for session in center["sessions"]:
                if session["min_age_limit"] <= age:
                  #  result.append(center["name"])
                    print("\t", center["name"])
                    print("\t", center["block_name"])
                   # result.append("\t", center["block_name"])
                    print("\t Price: ", center["fee_type"])
                    print("\t Available Capacity: ",
                          session["available_capacity"])
                    print("\t Available Dose 1: ",
                          session["available_capacity_dose1"])
                    print("\t Available Dose 2: ",
                          session["available_capacity_dose2"])
                    if(session["vaccine"] != ''):
                        print("\t Vaccine: ", session["vaccine"])
                    print("\n\n")

    else:
        print("No available slots on ", systemDate)
json_text = json.loads(response.text)

#print(json_text["centers"])
print(result)
#test = telegram_bot_sendtext("Hi Ashit ")
# print(test)
