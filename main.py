#pip install python-dotenv && pip install apscheduler
import requests
import time
import os
import logging
from dotenv import load_dotenv
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
load_dotenv() #Load .env file into system
scheduler = BackgroundScheduler()

def shutdown():
    logging.info("Suspend called")
    os.system('systemctl poweroff')

def call_api():
    logging.info("Call API...")
    dt_object = datetime.now()
    header_var = { "token": os.environ["ES_TOKEN"] }
    response = requests.get("https://developer.sepush.co.za/business/2.0/area?id=" + os.environ["ES_LOCID"], headers=header_var)
    data = response.json()
    if (len(data["events"]) > 0):
        dt_object = datetime.fromisoformat(data["events"][0]["start"])
        dt_object = dt_object - timedelta(minutes=5)
        scheduler.add_job(shutdown, 'cron', year=dt_object.year, month=dt_object.month, day= dt_object.day, hour=dt_object.hour, minute=dt_object.minute, id='shutdown', replace_existing=True)
        logging.info("Shutdown scheduled for " + dt_object.strftime("%H:%M:%S"))
    else: #If Loadshedding cancelled, then stop shutdown from occurring
        scheduler.remove_job('shutdown')

logging.basicConfig(filename="/home/tertiusvdg/shutdown_execution.log", level=logging.DEBUG, format="%(asctime)s %(message)s")
call_api()
scheduler.add_job(call_api,'interval', minutes=60, id='call_api')
scheduler.start()
while True:
    time.sleep(60)
