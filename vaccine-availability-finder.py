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
import logging.handlers as handlers
import argparse
import pickle

parser = argparse.ArgumentParser()
parser.add_argument("district_id", type=int, help='an integer for district id ')
parser.add_argument("age", type=int, help='an integer for the user age')
parser.add_argument("--refresh", type=int, help='an optional integer for the refresh frequency. default is 5 sec, '
                                                'excepted value: 5, 10, 15, 20, 25, 30')
parser.add_argument("--chatId", type=int, help='an optional integer for the telegram chat id ')
args = parser.parse_args()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
fmt = '%(asctime)s : %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt=fmt, datefmt='%m/%d/%Y %I:%M:%S %p')

logHandler = handlers.TimedRotatingFileHandler('app-prod-' + str(args.district_id) + '.log', when="H",
                                               interval=12)
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

save_state_timer = 0
centerList_Global = []


def cowinApiCall(district_id, age, chatId):
    age_group = "18 to 44" if age < 45 else "above 45"
    # default chatId (-1001172971393) - (cowin U45 Blore-Dev) if chatID is not provided
    channel_chatId = "-1001172971393" if chatId is None else chatId
    logger.info('-------xxxxxx------Started cowinApiCall ---------xxxxxxx------ for district id '
                + str(district_id) + ' and age group ' + age_group + "  chat id : " + str(channel_chatId) + '\n')
    temp_user_agent = UserAgent()
    browser_header = {'User-Agent': temp_user_agent.random,
                      'Cache-Control': 'no-cache',
                      'Pragma': 'no-cache'}
    systemDate = datetime.today().strftime('%d-%m-%Y')
    # district_id = 294  # 294- BBMP
    centerList = []
    global session_id
    global centerList_Global

    getStatesListUrl = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    calendarByDistrictUrl = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
    if len(centerList_Global) == 0:
        retrieveGlobalListState(district_id)

    queryparam = {'district_id': district_id, 'date': systemDate}
    try:
        response = requests.get(calendarByDistrictUrl,
                                headers=browser_header, params=queryparam, timeout=2)
        logger.info('response: ' + str(response))
        if response.status_code == 200:
            resp_json = response.json()
            if 'centers' in resp_json:
                logger.debug('Available on: ' + str(systemDate) +
                             ' for ' + age_group + ' age group ,user age: ' + str(age))
                for center in resp_json["centers"]:
                    for session in center["sessions"]:
                        if session["min_age_limit"] <= age:
                            name = center["name"]
                            block = center["block_name"]
                            district = center["district_name"]
                            pincode = center["pincode"]
                            feeType = center["fee_type"]
                            capacity = session["available_capacity"]
                            dose1 = session["available_capacity_dose1"]
                            dose2 = session["available_capacity_dose2"]
                            logger.debug('\t ' + center["name"])
                            logger.debug('\t ' + center["block_name"])
                            logger.debug('\t Price: ' + center["fee_type"])
                            logger.debug('\t Available Capacity: ' +
                                         str(session["available_capacity"]))
                            logger.debug('\t Available Dose 1: ' +
                                         str(session["available_capacity_dose1"]))
                            logger.debug('\t Available Dose 2: ' +
                                         str(session["available_capacity_dose2"]))
                            sessionId = session["session_id"]
                            logger.debug('\t session ID : ' +
                                         str(session["session_id"]))
                            if (session["vaccine"] != ''):
                                logger.debug('\t Vaccine: ' + session["vaccine"])
                                vaccine = session["vaccine"]
                            logger.debug('\t min age limit : ' +
                                         str(session["min_age_limit"]))
                            logger.debug('\t date: ' +
                                         str(session["date"]))
                            ageLimit = session["min_age_limit"]
                            date = session["date"]
                            logger.debug('----------------------------------- \n\n ')
                            centerList.append(
                                CenterInfo(name, block, district, pincode, feeType, capacity, dose1, dose2, sessionId,
                                           vaccine,
                                           ageLimit, date))
            else:
                logger.error("No available centers on ", systemDate)
        if centerList:
            for center in centerList:
                if isNotificationRequired(center):
                    logger.info(' slots available - sending telegram msg:  center name : ' + str(center.name) +
                                ' sessionId: ' + str(center.sessionId))
                    telegram_bot_sendtext("*" + center.name + "*" + "\n"
                                          + "pincode : " + str(center.pincode) + "\n"
                                          + center.blockName + " - " + center.district + "\n"
                                          + "vaccine : " + str(center.vaccine) + "\n"
                                          + "available capacity : " + str(center.capacity) + "\n"
                                          + "available Dose 1 : " + str(center.dose1) + "\n"
                                          + "available Dose 2 : " + str(center.dose2) + "\n"
                                          + "age limit : " + str(age_group) + "\n"
                                          + "Date : " + str(center.date) + "\n"
                                          + "CoWin : " + "_" + "https://selfregistration.cowin.gov.in/" + "_" + "\n"
                                          + "\U0001F489 \U0001F489",
                                          str(channel_chatId))
                    logger.info('-------------------------------------- \n\n ')
                else:
                    # telegram_bot_sendtext("No vaccine available at center " + center.name)
                    logger.debug("No vaccine available at center " + center.name)
                    logger.debug('-------------------------------------- \n\n ')
        else:
            logger.error("No available centers on ", systemDate)
        saveGlobalListState(district_id)
        logger.debug('-------xxxxxxxx--------- END of cowinApiCall ----------xxxxx--------- \n\n ')

    except requests.exceptions.HTTPError as errh:
        logger.info("Http Error:", str(errh))
    except (
            requests.ConnectionError,
            requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectTimeout
    ) as errc:
        logger.info("Error Connecting:", str(errc))
    except requests.exceptions.Timeout as errt:
        logger.info("Timeout Error:", str(errt))
    except requests.exceptions.RequestException as err:
        logger.info("OOps: Something Else", str(err))


def isNotificationRequired(center):
    global centerList_Global
    sentNotification = False
    logger.info("Start -- for centre:  " + center.name +
                " for date : " + str(center.date) + " : session id : " + center.sessionId +
                " | center capacity: " + str(center.capacity) + "  | dose 1 : " + str(
        center.dose1) + " | Dose 2 : " + str(center.dose2))
    logger.info("centerList_Global length : " + str(len(centerList_Global)))
    if centerList_Global:
        if center in centerList_Global:
            # if any(gl.sessionId == center.sessionId for gl in centerList_Global):
            saved_elements = getSavedCenter(center)
            logger.debug(" center present in global list: saved capacity : "
                        + str(saved_elements.capacity) + " center capacity : " + str(center.capacity))
            # global list contains center list
            # chk capacity if latest capacity > 1 then don't update the global list  nor sent notification
            if center.capacity > 2:
                if center.capacity > saved_elements.capacity + 50:
                    logger.debug("center capacity increased - Send Notification: updated global list")
                    updateCapacity(center)
                    sentNotification = True
                    logger.debug("centerList_Global size after updating : " + str(len(centerList_Global)))
                else:
                    logger.debug("new capacity not added - No Notification send ")
                    sentNotification = False
            elif center.capacity == 0:
                logger.debug("capacity is 0 all slots booked , remove it from global list and wait for new slots")
                logger.debug("remove from global list: len before: " + str(len(centerList_Global)))
                centerList_Global.remove(center)
                logger.debug("remove from global list: len after: " + str(len(centerList_Global)))
                sentNotification = False
        else:
            # if not present in global list and capacity > 1 add in global list and send notification
            if center.capacity > 2:
                logger.debug("Not present in global list and capacity > 0 add in global list and send notification")
                centerList_Global.append(center)
                sentNotification = True
            else:
                logger.debug("Not present in global list and capacity is 0 No action required")
    else:
        # if global list is empty then send notification if capacity >  1
        if center.capacity > 2:
            logger.debug("global list is empty then send notification for capacity > 0")
            sentNotification = True
            centerList_Global.append(center)
    logger.info("Notification required for the centre :" + center.name + " is: " + str(sentNotification) + '\n')
    logger.debug('-- End checking notification for centre: -------------' + center.name)
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
    systemDate = datetime.today().strftime('%d-%m-%Y')
    empty_list = []
    # 2 hours
    if save_state_timer == 0 or save_state_timer == 7200:
        outputFile = open('global_list_' + str(district_id) + '.dat', 'wb')
        pickle.dump(empty_list, outputFile)
        for center in centerList_Global:
            if center.date < systemDate:
                centerList_Global.remove(center)
        pickle.dump(centerList_Global, outputFile)
        outputFile.close()
        logger.info("state saved GlobalList size: " + str(len(centerList_Global)))
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
                logger.info(" retrieved Global list length : " + str(len(centerList_Global)))
            except EOFError:
                # When end of file has reached EOFError will be thrown
                # and we are setting endOfFile to True to end while loop
                endOfFile = True
    except FileNotFoundError:
        logger.debug("serialized File not found")
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
