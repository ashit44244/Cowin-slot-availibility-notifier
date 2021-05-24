# Cowin-slot-availibility-notifier

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
Prerequisite: Join the telegram public channel : cowin U45 Bangalore (https://t.me/cowinU45Bangalorearea) to receive the notification as soon as the slots are available
Once the application is started, user will start receiving notification in the above telegram channel.