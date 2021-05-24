# Cowin-slot-availibility-notifier

This is just a proof of concept project, it cannot book a slot automatically.
Public Cowin API details can be found here (https://apisetu.gov.in/public/marketplace/api/cowin/cowin-public-v2)

Currently, it can send telegram notification of the slots availability based on the ditrict_id and age provided, booking has to be done in the cowin portal only.
This tool just helps in getting notification as sonn as the slots get listed in the cowin portal. 

# Note 

Public APIs provided by CoWin app are currently not returning realtime slots. We strongly recommend you to visit https://selfregistration.cowin.gov.in to search & book directly.

List of states and corresponding districts can be fetched from the public api respectively
Grab the state id based on the state from the list of states : https://cdn-api.co-vin.in/api/v2/admin/location/states
Get the district ids based on the district by passing the state id in the placeholder : https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_id}

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/ashit44244/Cowin-slot-availibility-notifier.git
$ cd Cowin
```

install the dependencies:

```sh
$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies start the python worker by using 
the below cmd . It requires 2 mandatory parameters 1. district id 2. age:
```sh

$ python vaccine-availability-finder.py {district_id} {age}

example: python vaccine-availability-finder.py 294 32 


```
## Prerequisite:

Join the telegram public channel : cowin U45 Bangalore (https://t.me/cowinU45Bangalorearea) to receive the notification as soon as the slots are available
Once the application is started, user will start receiving notification in the above telegram channel.


## Testing

For Testing, it's recommended to use vaccine-availability-finder-dev.py : join telegram channel : cowin U45 Blore-Dev and start contributing





### Python 3.7.3 Installation in Windows
- Check if Python is already installed by opening command prompt and running ```python --version```.
- If the above command returns ```Python <some-version-number>``` you're probably good - provided version number is above 3.6
- If Python's not installed, command would say something like: ```'python' is not recognized as an internal or external command, operable program or batch file.```
- If so, download the installer from: https://www.python.org/ftp/python/3.7.3/python-3.7.3-amd64.exe
- Run that. In the first screen of installer, there will be an option at the bottom to "Add Python 3.7 to Path". Make sure to select it.
- Open command prompt and run ```python --version```. If everything went well it should say ```Python 3.7.3```
- You're all set! 

[![license](https://img.shields.io/github/license/DAVFoundation/captain-n3m0.svg?style=flat-square)](https://github.com/DAVFoundation/captain-n3m0/blob/master/LICENSE)
