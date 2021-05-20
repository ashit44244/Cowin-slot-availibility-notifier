import requests
import json
#from telegram_bot_rest_call_bot import telegram_bot_sendtext
from datetime import datetime
from fake_useragent import UserAgent
#from CenterDetails import CenterDetails

temp_user_agent = UserAgent()
browser_header = {'User-Agent': temp_user_agent.random}

systemDate = datetime.today().strftime('%d-%m-%Y')
district_id = 294  # 294- BBMP
age = 32
centerList =[]

getStatesListUrl = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
calendarByDistrictUrl = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict"

queryparam = {'district_id': district_id, 'date': systemDate}

try:
    response = requests.get(calendarByDistrictUrl,
                        headers=browser_header, params=queryparam, timeout= 0.00001)
    response.raise_for_status()
except requests.exceptions.HTTPError  as error:
    print(error)
    print(response)
    if response.ok:
        resp_json = response.json()
        if resp_json["centers"]:
            print("Available on: ", systemDate, "for 18-45 age group ,user age: ",age)
            for center in resp_json["centers"]:
                for session in center["sessions"]:
                    if session["min_age_limit"] <= age:
                        name = center["name"]
                        block = center["block_name"]
                        pincode = center["pincode"]
                        feeType = center["fee_type"]
                        capacity = center["available_capacity"]
                        dose1 = center["available_capacity_dose1"]
                        dose2 = center["available_capacity_dose2"]
                        print("\t", center["name"])
                        print("\t", center["block_name"])
                        print("\t", center["pincode"])
                        print("\t Price: ", center["fee_type"])
                        print("\t Available Capacity: ",
                            session["available_capacity"])
                        print("\t Available Dose 1: ",
                            session["available_capacity_dose1"])
                        print("\t Available Dose 2: ",
                            session["available_capacity_dose2"])
                        if(session["vaccine"] != ''):
                            print("\t Vaccine: ", session["vaccine"])
                            vaccine = center["vaccine"] 
                        print("\n\n")  
                        centerList.append (CenterDetails(name, block, pincode,feeType, capacity,dose1, dose2, vaccine)) 

        else:
            print("No available slots on ", systemDate)
    else:
            print("server not responding")


print(centerList)


