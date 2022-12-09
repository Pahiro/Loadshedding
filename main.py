import requests
import time
import os
import logging
from datetime import datetime, timedelta 
from apscheduler.schedulers.background import BackgroundScheduler

dt_object = datetime.now()

scheduler = BackgroundScheduler()

def shutdown():
    logging.info("Shutdown called")
    os.system('systemctl poweroff') 

def call_api():
    logging.info("Call API...")
    logging.info(dt_object)
    header_var = { "token":"11FC5D19-9D444406-B72C0B37-7EE96BBE" }
    response = requests.get("https://developer.sepush.co.za/business/2.0/area?id=tshwane-3-waterkloofpark", headers=header_var)
    data = response.json()
    dt_object = datetime.fromisoformat(data["events"][0]["start"])
    dt_object = dt_object - timedelta(minutes=5)
    #scheduler.add_job(shutdown, 'cron', year=2022, month=12, day=8, hour=23, minute=6, id='shutdown')
    scheduler.add_job(shutdown, 'cron', year=dt_object.year, month=dt_object.month, day= dt_object.day, hour=dt_object.hour, minute=dt_object.minute, id='shutdown')

scheduler.add_job(call_api,'interval', minutes=30, id='call_api')
scheduler.start()
while True:
    time.sleep(60)