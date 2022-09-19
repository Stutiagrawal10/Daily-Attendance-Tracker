from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import os
from dotenv import load_dotenv

class Bot():
    def __init__(self) -> None:
        load_dotenv()
        self.GEMS_EMAIL = os.getenv('GEMS_EMAIL')
        self.GEMS_PASSWORD = os.getenv('GEMS_PASSWORD')
        self.SENDERS_EMAIL = os.getenv('SENDERS_EMAIL')
        self.SENDERS_PASSWORD = os.getenv('SENDERS_PASSWORD')

    def track_attendance(self):
        PATH = 'C:\Program Files (x86)\chromedriver.exe'
        driver = webdriver.Chrome(PATH)

        driver.get("https://rcoem.in/login.htm")

        driver.find_element(By.ID,"j_username").send_keys(self.GEMS_EMAIL)
        driver.find_element(By.ID,"password-1").send_keys(self.GEMS_PASSWORD)
        driver.find_element(By.ID,"password-1").send_keys(Keys.RETURN)

        driver.find_element(By.ID,"stud2").click() 

        time.sleep(10)

        table_element = driver.find_element(By.XPATH,'/html/body/div[14]/div/div/div[1]/div[1]/div[1]/div[3]/table')
        table_element.screenshot('table.png')
        rows = table_element.find_elements(By.TAG_NAME,'tr')

        attendace =  rows[-1].find_element(By.XPATH,'./th[3]').text
        driver.close()

        return attendace

    def send_email(self, attendance):
        msgRoot = MIMEMultipart('related')

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgText = MIMEText(f'Daily Updated Gems Attendance: {attendance}%')
        msgAlternative.attach(msgText)

        fp = open('table.png', 'rb') #Read image 
        msgImage = MIMEImage(fp.read())
        fp.close()

        msgImage.add_header('Content-ID', '<image1>')
        msgRoot.attach(msgImage)

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(self.SENDERS_EMAIL,self.SENDERS_PASSWORD)
        server.sendmail(self.SENDERS_EMAIL,self.GEMS_EMAIL,msgRoot.as_string())
        server.quit()

