import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def getEmailAddrs():
    with open("emails.txt", "r") as emailFile:
        emails = emailFile.read()
    return emails


def sendEmail(bodyText):
    # The following 5 variables need to be changed to match an email that will be used to send the notificatin emails
    sender = 'name1@gmail.com'
    password = 'pass'
    server = 'gmail.server'
    port = 123
    username = 'username'

    server = smtplib.SMTP_SSL(server, port)
    server.login(username, password)

    message = MIMEMultipart()

    message['From'] = sender
    message['To'] = getEmailAddrs()
    message['Subject'] = 'Covid Vaccine Availability'
    message.attach(MIMEText(bodyText, 'plain'))

    server.send_message(message)


found_appointment = False
link = "https://am-i-eligible.covid19vaccine.health.ny.gov"

# This path to the chromedriver must be edited so that it represents the path in your local machine
driver = webdriver.Chrome(executable_path='/Applications/chromedriver')  # if you want to use chrome, replace Firefox() with Chrome()
getWeb = driver.get(link)

city_dict_glob = {}
first_iter = True
while True:
    driver.refresh()
    elem = driver.find_element(By.ID, 'root')
    # Timer to ensure website fully loads content, and to avoid overloading their servers with pings.
    time.sleep(5)
    innerHtml = elem.get_attribute('innerHTML')
    html_soup = BeautifulSoup(innerHtml, 'html.parser')
    soup = html_soup.find_all('td')
    # Verify that the website correctly loaded the table of sites
    if len(soup) > 0 and len(soup) % 3 == 0:
        # Populate a dictionary of sites and availabilities
        city_dict = {}
        for i in range(0, len(soup), 3):
            city_dict[soup[i].string] = [soup[i + 1].string, soup[i + 2].string]

        # Cycle through each site and verify check if it has newly become available
        for site in city_dict:
            # Get the three conditions for sending an email
            currAvailable = city_dict[site][1] == 'Appointments Available'
            if first_iter:
                prevNotAvail = False
            # This covers possibility that they add a new site
            elif site not in city_dict_glob:
                prevNotAvail = True
            else:
                prevNotAvail = city_dict_glob[site][1] != 'Appointments Available'
            notSpecialSite = not (site[0:2] == '**')

            #  Send an email and print output to console
            if currAvailable and prevNotAvail and notSpecialSite:
                outputText = 'Appointments Available in ' + site + '. Go to ' + link + ' immediately.'
                sendEmail(outputText)
                print(outputText)
                found_appointment = True
        # This dictionary is used to compare the previous state of all sites
        city_dict_glob.clear()
        city_dict_glob = city_dict.copy()

    # If nothing was found, or the website wasn't loaded properly, print to console.
    if not found_appointment:
        print('No Appointments Found')
    first_iter = False
