#!/usr/bin/env python3
import requests
import json
from datetime import datetime
from telegram_bot_rest_call_bot import *
from fake_useragent import UserAgent
from CenterDetails import CenterInfo
import schedule
import time
import logging

logging.basicConfig(filename='myapp-prod.log', format='%(asctime)s : %(levelname)s - %(message)s', level=logging.INFO,
                    datefmt='%m/%d/%Y %I:%M:%S %p')

session_id = "none"
centerList_Global = []


def cowinApiCall():
    logging.info('-------------Started ---------------')
    temp_user_agent = UserAgent()
    browser_header = {'User-Agent': temp_user_agent.random}
    systemDate = datetime.today().strftime('%d-%m-%Y')
    district_id = 294  # 294- BBMP
    age = 32
    centerList = []
    global session_id
    global centerList_Global

    getStatesListUrl = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    calendarByDistrictUrl = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict"

    queryparam = {'district_id': district_id, 'date': systemDate}

    try:
        response = requests.get(calendarByDistrictUrl,
                                headers=browser_header, params=queryparam)
        logging.info('------------------------  response: ' + str(response))
        if response.ok:
            resp_json = response.json()
            if resp_json["centers"]:
                logging.debug('Available on: ' + str(systemDate) +
                              ' for 18-45 age group ,user age: ' + str(age))
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
                            logging.debug('\t ' + center["name"])
                            logging.debug('\t ' + center["block_name"])
                            logging.debug('\t Price: ' + center["fee_type"])
                            logging.debug('\t Available Capacity: ' +
                                          str(session["available_capacity"]))
                            logging.debug('\t Available Dose 1: ' +
                                          str(session["available_capacity_dose1"]))
                            logging.debug('\t Available Dose 2: ' +
                                          str(session["available_capacity_dose2"]))
                            sessionId = session["session_id"]
                            logging.debug('\t Available Dose 2: ' +
                                          str(session["session_id"]))
                            if (session["vaccine"] != ''):
                                vaccine = session["vaccine"]
                                logging.debug('\t Vaccine: ' + session["vaccine"])
                            ageLimit = session["min_age_limit"]
                            date = session["date"]
                            logging.debug('\t min age limit : ' +
                                          str(session["min_age_limit"]))
                            logging.debug('\t date: ' +
                                          str(session["date"]))
                            logging.debug('----------------------------------- \n\n ')
                            centerList.append(
                                CenterInfo(name, block, pincode, feeType, capacity, dose1, dose2, sessionId, vaccine,
                                           ageLimit, date))
            # else:
            # logging.info("No available centers on ", systemDate)

        for center in centerList:
            if center.capacity > 0 and isCenterDetailsUpdated(center):
                logging.info(' slots available - sending telegram notification:  center name : ' + str(center.name) +
                             ' sessionId: ' + str(center.sessionId))
                telegram_bot_sendtext("Center : " + center.name + "\n"
                                      + "Block : " + center.blockName + "\n"
                                      + "pincode : " + str(center.pincode) + "\n"
                                      + "available capacity : " + str(center.capacity) + "\n"
                                      + "available Dose1 : " + str(center.dose1) + "\n"
                                      + "available Dose2 : " + str(center.dose2) + "\n"
                                      + "vaccine : " + str(center.vaccine) + "\n"
                                      + "age limit : " + str(center.ageLimit) + " to 44 " + "\n"
                                      + "Date : " + str(center.date) + "\n")
            else:
                # telegram_bot_sendtext("No vaccine available at center "+ center.name)
                logging.info("No vaccine available at center " + center.name)
        if centerList:
            centerList_Global = centerList
        logging.info('---------------- END ------------------- \n\n ')

    except requests.ConnectionError as err:
        logging.error("Connection error : " + err)


def isCenterDetailsUpdated(center):
    global centerList_Global
    logging.debug("inside isCenterDetailsUpdated: length of global centre list: " + str(len(centerList_Global)))
    if centerList_Global:
        is_Updated = False
        for savedCenter in centerList_Global:
            # unique id for center name (center name + date)
            savedId = savedCenter.name + "-" + savedCenter.date
            centerId = center.name + "-" + center.date
            if savedId == centerId:
                logging.info("checking for center : " + centerId + " saved session id: "
                             + savedCenter.sessionId + " current session id: " + center.sessionId)
                if savedCenter.sessionId != center.sessionId:
                    logging.info("ID Updated - send notification ")
                    is_Updated = True
                else:
                    logging.info("ID Not Updated - No notification ")
                    is_Updated = False
        return is_Updated
    else:
        return True


cowinApiCall()

# scheduler to call cowin api after x sec 
schedule.every(15).seconds.do(cowinApiCall)

while True:
    schedule.run_pending()
    time.sleep(1)
