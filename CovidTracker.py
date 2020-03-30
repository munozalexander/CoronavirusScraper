from selenium import webdriver
from time import sleep
import re
from datetime import datetime
from selenium.webdriver.common.by import By
import smtplib
#source venv/bin/activate

class Coronavirus():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.states = ['Massachusetts', 'Texas', 'New York']
        self.emails = ['XXX@gmail.com']

    def scrapeData(self):
        self.driver.get('https://www.worldometers.info/coronavirus/country/us/')
        data = {}
        table = self.driver.find_element(By.ID, 'usa_table_countries_yesterday')
        body = table.find_element(By.TAG_NAME, "tbody")
        rows = body.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            col = row.find_elements(By.TAG_NAME, "td")
            col = [c.get_attribute('innerText').strip() for c in col]
            state = col[0]
            if state in self.states:
                data[state] = {}
                data[state]['total_cases'] = col[1]
                data[state]['new_cases'] = col[2] if col[2]!='' else '0'
                data[state]['total_deaths'] = col[3]
                data[state]['new_deaths'] = col[4] if col[4]!='' else '0'
                data[state]['active_cases'] = col[5]
        for d in data:
            print d, "=>", data[d]
        self.sendEmail(data)
        self.driver.close()

    def sendEmail(self, data):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('munoz.coding@gmail.com', 'iCUQ3xG4bwusRY')
        subject = 'Newly Scraped Coronavirus Data'
        body = ''
        for state in self.states:
            body += 'Yesterday in ' + state + '\
                \nNew cases yesterday: ' + data[state]['new_cases'] +'\
                \nTotal cases: ' + data[state]['total_cases'] + '\
                \nNew deaths yesterday: ' + data[state]['new_deaths'] + '\
                \nTotal deaths: ' + data[state]['total_deaths'] + '\
                \nActive cases: ' + data[state]['active_cases'] + '\
                \n\n'
        body += 'Stay safe!\n-Your coronavirus bot'
        msg = "Subject: %s\n\n%s" % (subject,body)
        for email in self.emails:
            server.sendmail(
                'munoz.coding@gmail.com',
                email,
                msg
            )
        print 'Emails sent.'
        server.quit()

bot = Coronavirus()
bot.scrapeData()
