from cryptography.fernet import Fernet
from twilio.rest import Client
from selenium import webdriver
from time import sleep, ctime
from random import randint
from json import dumps, loads
from pathlib import Path
import datetime, os

class SetUp:
    def __init__(self):
        self.file_path = Path(__file__)
        self.current_dir = self.file_path.parent.absolute()
        self.retriveCredentials()

    # Retrive user creds
    def retriveCredentials(self):
        reset_msg = "username     : username\npassword     : password\naccount_sid  : account_sid\nauth_token   : auth_token\ntwilio_phone : twilio_phone\nusr_phone    : usr_phone"
        self.credentials = {}
        with open(str(self.current_dir)+'/credentials.txt', 'r') as f:
            creds_list= f.read().split('\n')
            for i in creds_list:
                if i.strip(' ') != '':
                    self.credentials[i.split(":")[0].strip(' ')] = i.split(":")[1].strip(' ')

        # Reset credentials.txt
        with open(str(self.current_dir)+'/credentials.txt', 'w') as f:
            f.write(reset_msg)
   
    def encryption(self):
        plaintext = dumps(self.credentials).encode('utf-8')
        key = Fernet.generate_key()

        self.token = Fernet(key)
        self.credentials = self.token.encrypt(plaintext)

    def getCredentials(self):
        plaintext = loads(self.token.decrypt(self.credentials).decode('utf-8'))
        return plaintext

class Attendance_System:
    def __init__(self, username, password, account_sid, auth_token, twilio_phone, usr_phone):
        self.username = username
        self.password = password
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.twilio_phone = twilio_phone
        self.usr_phone = usr_phone
    
    def notification(self, msg):
        Twilio_SID = self.account_sid
        Auth_Token = self.auth_token
        client = Client(Twilio_SID, Auth_Token)

        message = client.messages \
                        .create(
                            body = msg,
                            from_ = self.twilio_phone,
                            to = self.usr_phone
                        )

    def log_in(self):
        # Go to FYPJ 2.0 Website
        self.driver = webdriver.Chrome()
        self.driver.get('https://fypj.sit.nyp.edu.sg/')
        self.driver.implicitly_wait(10)

        # Enter Username
        self.driver.find_element('xpath','/html/body/div/div/div/div/div[2]/form/fieldset/div[2]/input').send_keys(self.username)
        # Enter Password
        self.driver.find_element('xpath','/html/body/div/div/div/div/div[2]/form/fieldset/div[3]/input').send_keys(self.password)
        self.driver.find_element('xpath','/html/body/div/div/div/div/div[2]/form/fieldset/div[6]/input[2]').click()

    def check_in(self):
        self.log_in()
        
        # Click on Student Dropdown Button
        self.driver.find_element('xpath', '/html/body/form/div[3]/nav/div/div[2]/ul[1]/li[1]/a').click()
        # Click on Sign In/Out
        self.driver.find_element('xpath', '/html/body/form/div[3]/nav/div/div[2]/ul[1]/li[1]/ul/li[1]/a').click()
        # Check In the system
        self.driver.find_element('xpath', '//*[@id="form1"]/div[3]/div[2]/div[5]/div/div/div[4]/div[2]').click()
        # Click Confirmation
        self.driver.find_element('xpath', '//*[@id="ContentPlaceHolder1_btn_ok"]').click()

        self.notification("You have Successfully Checked Into the FYPJ System at " + ctime())
        self.driver.close()        

    def check_out(self):
        self.log_in()
        
        # Click on Student Dropdown Button
        self.driver.find_element('xpath', '/html/body/form/div[3]/nav/div/div[2]/ul[1]/li[1]/a').click()
        # Click on Sign In/Out
        self.driver.find_element('xpath', '/html/body/form/div[3]/nav/div/div[2]/ul[1]/li[1]/ul/li[1]/a').click()
        # Check Out of the system
        self.driver.find_element('xpath', '/html/body/form/div[3]/div[2]/div[5]/div/div/div[4]/div[3]/input').click()
        # Click Confirmation
        self.driver.find_element('xpath', '/html/body/form/div[3]/div[2]/div[8]/div/div/div[3]/button').click()

        self.notification("You have Successfully Checked Out of the FYPJ System at " + ctime())
        self.driver.close()

if __name__ == '__main__':
    #Setup for script
    user_instance = SetUp()
    user_instance.encryption()
    credentials = user_instance.getCredentials()
    system_instance = Attendance_System(credentials["username"], credentials["password"],credentials["account_sid"],credentials["auth_token"],credentials["twilio_phone"],credentials["usr_phone"])
    print("System Initialized: Starting System\n===== Welcome user {}! =====".format(credentials["username"]))

    

    while True:
        current_time = datetime.datetime.now()
        # Set Checkout time to 5,30pm on fridays and 6pm on other weekdays (require fixing)
        # checkout = datetime.time(17,30,0) if current_time.isoweekday() == 5 else datetime.time(18,0,0)

        # Check if today is Monday - Friday
        if current_time.isoweekday() in range(1, 6):
            # Trigger Check In Function after 8.00 am
            if datetime.time(8,0,0) <= current_time.time() <= datetime.time(8,30,59):
                # Emulate human's randomness (Up to 20 mins)  
                sleep(randint(1,1200))
                try:
                    system_instance.check_in()
                    print("Successfully Checked In on " + ctime())
                except Exception as e:
                    system_instance.notification(f"You have Failed to Check Into the FYPJ System at {ctime()}\n\n ERROR Code: {e}" )

                sleep(21600)
            # Trigger Check Out Function after 6.00pm / 5.30pm
            elif datetime.time(18,0,0) <= current_time.time() <= datetime.time(18,10,59):
            # elif checkout <= current_time.time() <= (checkout + datetime.timedelta(minutes=10)).time():
                # Emulate human's randomness (Up to 4mins)  
                sleep(randint(1,240))
                try:
                    system_instance.check_out() 
                    print("Successfully Checked Out on " + ctime())
                except Exception as e:
                    system_instance.notification(f"You have Failed to Check Out of the FYPJ System at {ctime()}\n\n ERROR Code: {e}" )
                
                sleep(21600)
            # Stop the script for 5 mins
            else:
                sleep(300)     
        # Stop Running the code on Saturday and Sunday by pausing the code every 6 hours:
        else:
            sleep(21600)
            continue
        