#!/usr/bin/env python3
import requests
import json
from datetime import datetime
from telegram_bot_rest_call_bot import *
from fake_useragent import UserAgent
from CenterDetails import CenterInfo


def cowinApiCall():
    temp_user_agent = UserAgent()
    browser_header = {'User-Agent': temp_user_agent.random}
    systemDate = datetime.today().strftime('%d-%m-%Y')
    district_id = 294  # 294- BBMP
    age = 32
    centerList = []

    getStatesListUrl = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    calendarByDistrictUrl = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict"

    queryparam = {'district_id': district_id, 'date': systemDate}

    response = requests.get(calendarByDistrictUrl,
                            headers=browser_header, params=queryparam)
    if response.ok:
        resp_json = response.json()
        if resp_json["centers"]:
            for center in resp_json["centers"]:
                for session in center["sessions"]:
                    if session["min_age_limit"] <= age:
                        name = center["name"]
                        block = center["block_name"]
                        pincode = center["pincode"]
                        feeType = center["fee_type"]
                        capacity = session["available_capacity"]
                        dose1 = session["available_capacity_dose1"]
                        dose2 = session["available_capacity_dose2"]
                        if(session["vaccine"] != ''):
                            vaccine = session["vaccine"]
                        ageLimit = session["min_age_limit"]
                        date = session["date"]
                        centerList.append(CenterInfo(name, block, pincode, feeType, capacity, dose1, dose2, vaccine,ageLimit, date))
        #else:
            #print("No available centers on ", systemDate)

    for center in centerList:
        if center.capacity != 0:
            telegram_bot_sendtext("Center : " + center.name + "\n"
                              + "Block : " + center.blockName + "\n"
                              + "pincode : " + str(center.pincode) + "\n"
                              + "fee type : " + str(center.feeType) + "\n"
                              + "available capacity : " + str(center.capacity) + "\n"
                              + "Dose1 : " + str(center.dose1) + "\n"
                              + "Dose2 : " + str(center.dose2) + "\n"
                              + "vaccine : " + str(center.vaccine) + "\n"
                              + "age limit : " + str(center.ageLimit) + "\n"
                              + "Date : " + str(center.date) + "\n")
        #else:
            #telegram_bot_sendtext("No vaccine available at center "+ center.name)

cowinApiCall()