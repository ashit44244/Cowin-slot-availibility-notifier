import schedule
import time


def printer():
  print("---------------------Hello World !! ---------------------- ")



schedule.every(5).seconds.do(printer)

while True:
    schedule.run_pending()
    time.sleep(1)