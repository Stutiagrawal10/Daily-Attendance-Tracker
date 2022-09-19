from attendance_tracker import Bot
from time import sleep
from datetime import datetime

bot = Bot()

while True:
    attendance = bot.track_attendance()
    bot.send_email(attendance)
    print(f"{datetime.now()} : {attendance}%")
    sleep(24*60*60 - 60)
    