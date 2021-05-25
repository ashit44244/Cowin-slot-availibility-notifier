# Cowin-slot-availibility-notifier

This is just a proof of concept project, it cannot book a slot automatically.
Public Cowin API details can be found here (https://apisetu.gov.in/public/marketplace/api/cowin/cowin-public-v2)

Currently, it can send telegram notification of the slots availability based on the district_id and age provided, booking has to be done in the cowin portal only.
This tool just helps in getting notification as soon as the slots get listed in the Cowin portal. 

# Note 

Public APIs provided by CoWin app are currently not returning realtime slots. We strongly recommend you to visit https://selfregistration.cowin.gov.in to search & book directly.
List of states and corresponding districts can be fetched from the public api respectively

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/ashit44244/Cowin-slot-availibility-notifier.git
$ cd Cowin-slot-availibility-notifier
```

install the dependencies:

```sh
$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies start the python worker by using 
the below cmd . It requires 2 mandatory parameters and 1 optional  1. district id 2. age 3. channel_chat_id
Default chat is for cowin U45 Blore-Dev. 

## Find district id for your area

Step 1: Hit the api in browser: https://cdn-api.co-vin.in/api/v2/admin/location/states
Step 2: It will show the list of all states along with the state id as shown below:
![state-list](img/states.PNG?raw=true)

Step 3: Grab the state id for your state.
Step 4: Hit the api in browser as shown below: https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_id}

Example: Get all district in maharashtra :  https://cdn-api.co-vin.in/api/v2/admin/location/districts/21

![state-list](img/district.PNG?raw=true)

Step 4: Grab the district id for your region example: For pune it's 363

## New Telegram channel for your Region

Step 1: Create a new channel like cowin U45 {region name}. Once channel is created, go to add members and add cowinUnder45bot
to the channel and make it as admin.

![telegram_channel-1](img/telegram-1.PNG?raw=true)
![telegram_channel-2](img/telegram-2.PNG?raw=true)
![telegram_channel-3](img/telegram-3.PNG?raw=true)
![telegram_channel-4](img/telegram-4.PNG?raw=true)

Step 2: Hit the api in browser - https://api.telegram.org/bot1755134661:AAE4ysHFi75lUqF2o2H_Fs3Or3jHDlfKUjM/getUpdates
 and search for your channel in the result as shown below, 

![getUpdates api](img/get_updates_api.PNG?raw=true)

Step 3: Grab the chat id for your channel as shown above. Now you are ready to run the worker



```sh

$ python vaccine-availability-finder.py {district_id} {age} {channel_chat_id}

example:
python vaccine-availability-finder.py 363 32 --chatId -1001463113416
-1001463113416 is the chat if for cowin U45 Pune telegram channel


```
#### Note Cowin U45 Pune is only used as an example, it's not functional as of now.

### Anyone willing to contribute can start a new channel for their region by following the above steps and can help people in their region to get vax availability notification.

## Telegram channel for Bangalore:

Worker for Telegram channel is handled by me, and it's fully functional. 
Join the telegram public channel : cowin U45 Bangalore (https://t.me/cowinU45Bangalorearea) to receive the notification as soon as the slots are available
Once the application is started, user will start receiving notification in the above telegram channel.


## Testing

For Testing, it's recommended to use vaccine-availability-finder-dev.py : join telegram channel : cowin U45 Blore-Dev and start contributing

```sh

$ python vaccine-availability-finder.py {district_id} {age}

example:
python vaccine-availability-finder.py 363 32 --chatId -1001172971393 
-1001172971393 is the chat Id for cowin U45 Blore-Dev telegram channel


```

#### drop me message on telegram for any support or help: @ashit44244(https://t.me/ashit44244)


## Prerequisite:
### Python 3.7.3 Installation in Windows
- Check if Python is already installed by opening command prompt and running ```python --version```.
- If the above command returns ```Python <some-version-number>``` you're probably good - provided version number is above 3.6
- If Python's not installed, command would say something like: ```'python' is not recognized as an internal or external command, operable program or batch file.```
- If so, download the installer from: https://www.python.org/ftp/python/3.7.3/python-3.7.3-amd64.exe
- Run that. In the first screen of installer, there will be an option at the bottom to "Add Python 3.7 to Path". Make sure to select it.
- Open command prompt and run ```python --version```. If everything went well it should say ```Python 3.7.3```
- You're all set! 

[![license](https://img.shields.io/github/license/DAVFoundation/captain-n3m0.svg?style=flat-square)](https://github.com/DAVFoundation/captain-n3m0/blob/master/LICENSE)
