# NYS-COVID-Vaccine-Notifications
This code was created in February 2021 in order to repeatedly check the NYS COVID Vaccination website ``` https://am-i-eligible.covid19vaccine.health.ny.gov``` every 5 seconds. It send emails to a predetermined list of people, notifying them when a vaccination site which previously had no openings, is updated with new openings. This program is meant to run continuously on a machine. Annoyingly, since NYS updates the website structure every now and then, this code needs to be updated accordingly. However, after vaccines began to become widely available, this project was abandoned.

# Requirements
Install Beautifulsoup 4 using:
```
$ pip install beautifulsoup4
```
Install selenium (```https://pythonspot.com/selenium-install/```) using:
```
pip install -U selenium
```
Download/Update your Chrome Browser, the download the latest Chrome webdriver, ```https://sites.google.com/a/chromium.org/chromedriver/downloads``` and add it to your applications folder.

Update emails.txt with the list of people you wish to notify of new openings. The emails should be separated with commas. 

Update nys_covid.py to include the email account information which you will use to send out the email notifications. An account with fewer security features (multifactor authentication, etc) is preferable for authentication reasons. The lines which need to be edited are clearly noted in the code comments. 

Update nys_covid.py with the correct foilder path to your local chromedriver. Once again, this is noted in the code comments. 

# Running
Open a terminal window in this respository. Then run:
```
python3 nys_covid.py
```
Occasionally, the progam might crash due to internet connectivtity problems, etc. So it is a good idea to check up on it every now and then to make sure it did not crash. It can simply be run again if need be. 
