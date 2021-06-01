#!/usr/bin/env python3
import requests
import json
from datetime import datetime
from telegram_bot_rest_call_bot import *
# from telegram_bot_test_env import *
from fake_useragent import UserAgent
from CenterDetails import CenterInfo
import schedule
import time
import logging
import argparse
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("district_id", type=int, help='an integer for district id ')
parser.add_argument("age", type=int, help='an integer for the user age')
parser.add_argument("--refresh", type=int, help='an optional integer for the refresh frequency. default is 5 sec, '
                                                'excepted value: 5, 10, 15, 20, 25, 30')
parser.add_argument("--chatId", type=int, help='an optional integer for the telegram chat id ')
args = parser.parse_args()


logging.basicConfig(filename='app-prod-' + str(args.district_id) + '.log',
                    format='%(asctime)s : %(levelname)s - %(message)s', level=logging.INFO,
                    datefmt='%m/%d/%Y %I:%M:%S %p')
save_state_timer = 0
centerList_Global = []


def cowinApiCall(district_id, age, chatId):
    age_group = "18 to 44" if age < 45 else "above 45"
    # default chatId (-1001172971393) - (cowin U45 Blore-Dev) if chatID is not provided
    channel_chatId = "-1001172971393" if chatId is None else chatId
    logging.info('-------xxxxxx------Started cowinApiCall ---------xxxxxxx------ for district id '
                 + str(district_id) + ' and age group ' + age_group + "  chat id : " + str(channel_chatId) + '\n')
    temp_user_agent = UserAgent()
    browser_header = {'User-Agent': temp_user_agent.random}
    systemDate = datetime.today().strftime('%d-%m-%Y')
    # district_id = 294  # 294- BBMP
    centerList = []
    global session_id
    global centerList_Global

    getStatesListUrl = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    calendarByDistrictUrl = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict"
    if len(centerList_Global) == 0:
        retrieveGlobalListState(district_id)

    queryparam = {'district_id': district_id, 'date': systemDate}
    try:
        response = requests.get(calendarByDistrictUrl,
                                headers=browser_header, params=queryparam, timeout=2)
        logging.info('response: ' + str(response))
        if response.status_code == 200:
            resp_json = response.json()
            if 'centers' in resp_json:
                logging.debug('Available on: ' + str(systemDate) +
                              ' for ' + age_group + ' age group ,user age: ' + str(age))
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
                            logging.debug('\t session ID : ' +
                                          str(session["session_id"]))
                            if (session["vaccine"] != ''):
                                logging.debug('\t Vaccine: ' + session["vaccine"])
                                vaccine = session["vaccine"]
                            logging.debug('\t min age limit : ' +
                                          str(session["min_age_limit"]))
                            logging.debug('\t date: ' +
                                          str(session["date"]))
                            ageLimit = session["min_age_limit"]
                            date = session["date"]
                            logging.debug('----------------------------------- \n\n ')
                            centerList.append(
                                CenterInfo(name, block, pincode, feeType, capacity, dose1, dose2, sessionId, vaccine,
                                           ageLimit, date))
            else:
                logging.error("No available centers on ", systemDate)
        if centerList:
            for center in centerList:
                if isNotificationRequired(center):
                    logging.info(' slots available - sending telegram msg:  center name : ' + str(center.name) +
                                 ' sessionId: ' + str(center.sessionId))
                    telegram_bot_sendtext("Center : " + center.name + "\n"
                                          + "Block : " + center.blockName + "\n"
                                          + "pincode : " + str(center.pincode) + "\n"
                                          + "available capacity : " + str(center.capacity) + "\n"
                                          + "available Dose1 : " + str(center.dose1) + "\n"
                                          + "available Dose2 : " + str(center.dose2) + "\n"
                                          + "vaccine : " + str(center.vaccine) + "\n"
                                          + "age limit : " + str(age_group) + "\n"
                                          + "Date : " + str(center.date) + "\n", str(channel_chatId))
                    logging.info('-------------------------------------- \n\n ')
                else:
                    # telegram_bot_sendtext("No vaccine available at center " + center.name)
                    logging.debug("No vaccine available at center " + center.name)
                    logging.debug('-------------------------------------- \n\n ')
        else:
            logging.error("No available centers on ", systemDate)
        saveGlobalListState(district_id)
        logging.debug('-------xxxxxxxx--------- END of cowinApiCall ----------xxxxx--------- \n\n ')

    except requests.exceptions.HTTPError as errh:
        logging.info("Http Error:", str(errh))
    except (
            requests.ConnectionError,
            requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectTimeout
    ) as errc:
        logging.info("Error Connecting:", str(errc))
    except requests.exceptions.Timeout as errt:
        logging.info("Timeout Error:", str(errt))
    except requests.exceptions.RequestException as err:
        logging.info("OOps: Something Else", str(err))


def isNotificationRequired(center):
    global centerList_Global
    sentNotification = False
    logging.info("Start -- for centre:  " + center.name +
                 " for date : " + str(center.date) + " : session id : " + center.sessionId +
                 " | center capacity: " + str(center.capacity) + "  | dose 1 : " + str(center.dose1) + " | Dose 2 : " + str(center.dose2))
    logging.info("centerList_Global length : " + str(len(centerList_Global)))
    if centerList_Global:
        if center in centerList_Global:
            # if any(gl.sessionId == center.sessionId for gl in centerList_Global):
            saved_elements = getSavedCenter(center)
            logging.info(" center present in global list: saved capacity : "
                          + str(saved_elements.capacity) + " center capacity : " + str(center.capacity))
            # global list contains center list
            # chk capacity if latest capacity > 1 then don't update the global list  nor sent notification
            if center.capacity > 1:
                if center.capacity > saved_elements.capacity:
                    logging.info("center capacity increased - Send Notification: updated global list")
                    updateCapacity(center)
                    sentNotification = True
                    logging.info("centerList_Global size after updating : " + str(len(centerList_Global)))
                else:
                    logging.info("new capacity not added - No Notification send ")
                    sentNotification = False
            elif center.capacity == 0:
                logging.info("capacity is 0 all slots booked , remove it from global list and wait for new slots")
                logging.info("remove from global list: len before: " + str(len(centerList_Global)))
                centerList_Global.remove(center)
                logging.info("remove from global list: len after: " + str(len(centerList_Global)))
                sentNotification = False
        else:
            # if not present in global list and capacity > 1 add in global list and send notification
            if center.capacity > 1:
                logging.info("Not present in global list and capacity > 0 add in global list and send notification")
                centerList_Global.append(center)
                sentNotification = True
            else:
                logging.info("Not present in global list and capacity is 0 No action required")
    else:
        # if global list is empty then send notification if capacity >  1
        if center.capacity > 1:
            logging.info("global list is empty then send notification for capacity > 0")
            sentNotification = True
            centerList_Global.append(center)
    logging.info("Notification required for the centre :" + center.name + " is: " + str(sentNotification) + '\n')
    logging.debug('-- End checking notification for centre: -------------' + center.name)
    return sentNotification


def getSavedCenter(center):
    for savedCenter in centerList_Global:
        if center == savedCenter:
            return savedCenter


def updateCapacity(center):
    for savedCenter in centerList_Global:
        if center == savedCenter:
            savedCenter.capacity = center.capacity


def saveGlobalListState(district_id):
    global centerList_Global
    global save_state_timer
    # 2 hours
    if save_state_timer == 0 or save_state_timer == 7200:
        outputFile = open('global_list_' + str(district_id) + '.dat', 'wb')
        pickle.dump(centerList_Global, outputFile)
        outputFile.close()
        logging.info("state saved GlobalList size: " + str(len(centerList_Global)))
        # reset the timer to zero
        save_state_timer = 0
    save_state_timer += 15


def retrieveGlobalListState(district_id):
    global centerList_Global
    try:
        inputFile = open('global_list_' + str(district_id) + '.dat', 'rb')
        endOfFile = False  # It is used to indicate end of file
        while not endOfFile:
            try:
                list = pickle.load(inputFile)
                centerList_Global = list
                logging.info(" retrieved Global list length : " + str(len(centerList_Global)))
            except EOFError:
                # When end of file has reached EOFError will be thrown
                # and we are setting endOfFile to True to end while loop
                endOfFile = True
    except FileNotFoundError:
        logging.debug("serialized File not found")
    else:
        inputFile.close()  # Close the file


cowinApiCall(args.district_id, args.age, args.chatId)

# scheduler to call cowin api after x sec

if args.refresh in {5, 10, 15, 20, 25, 30}:
    schedule.every(args.refresh).seconds.do(cowinApiCall, args.district_id, args.age, args.chatId)
else:
    schedule.every(5).seconds.do(cowinApiCall, args.district_id, args.age, args.chatId)

while True:
    schedule.run_pending()
    time.sleep(1)
