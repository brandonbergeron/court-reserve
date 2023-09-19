import time
from datetime import datetime
import schedule
import questionary
from utils.maps import courtMap, weekdayTimeMap, saturdayTimeMap, sundayTimeMap, days, months, dates
from utils.creds import loginPage, reservationUrl, userName, password
from utils.paths import closeXPath, submitXPath, resTypeXPath
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


test = input('Are you running in test mode? (y/n): ').lower().strip() == 'y'
numDrivers = int(questionary.text('How many browsers to boot up?').ask())
day = questionary.select(
     "Day: ",
     choices = days,
).ask()
targetMonth = questionary.select(
     "Month:",
     choices = months.values()).ask()
targetDate = questionary.select(
     "Date:",
     choices = dates,
     default = str(datetime.now().day)
).ask()
resType = questionary.select(
    "Select reservation type:",
    choices = [
        'Singles',
        'Doubles',
        'Ball Machine',
    ]).ask()
targetCourt = questionary.select(
    "Select a court:",
    choices = courtMap.keys()
    ).ask()
targetTime = questionary.select(
    "Select a time: ",
    choices = days[day].keys()
    ).ask()

driverContainer = {}

def createDriverDict(numDrivers: int):
    global driverContainer 
    
    for i in range(numDrivers):
        driverContainer[f'driver{i}'] = {
            'driver': webdriver.Chrome(),
            'button': None,
        }

    return driverContainer


def loginDriver(driver: webdriver):
    driver.get(loginPage)
    userNameField = driver.find_element(By.NAME, "UserNameOrEmail")
    passwordField = driver.find_element(By.NAME, 'Password')
    userNameField.send_keys(userName)
    passwordField.send_keys(password)
    loginButton = driver.find_element(By.CLASS_NAME, 'btn-log')
    loginButton.click()
    time.sleep(2)
    driver.get(reservationUrl)
    time.sleep(2)
    
    return driver


# Check for if desired date is not in current month
def calCheck(driver: webdriver):
    datePicker = driver.find_element(By.CSS_SELECTOR, ".k-icon.k-i-calendar")
    datePicker.click()
    time.sleep(2)

    currentMonth = str(datetime.now().date())[-5:-3]

    if (targetMonth != months[currentMonth[:2]]):
        nextButton = driver.find_element(By.CSS_SELECTOR, "[data-action='next']")
        nextButton.click()
        time.sleep(2)

    return driver


# Find date in calendar popup
def selectDate(driver: webdriver):
    calTable = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "k-content")))

    for row in calTable.find_elements(By.XPATH, "//tr"):
                for cell in row.find_elements(By.XPATH, "td"):
                    if (cell.text == targetDate):
                        dateElem = driver.find_element(By.LINK_TEXT, targetDate)
                        dateElem.click()
                        time.sleep(3)
    return driver
                    
timeSlotXPath = f"/html/body/div[1]/div[2]/div/div[2]/div/div/div/div/div/div/div/div/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[{days[day][targetTime]}]/td[{courtMap[targetCourt]}]/span/button"

def selectReservation(driver: webdriver):
    reservationSlot = driver.find_element(By.XPATH, timeSlotXPath)
    reservationSlot.click()
    time.sleep(2)

    return driver

def editReservation(driver: webdriver):
    # Singles, Doubles, or Ball Machine:
    reservationTypeSelector = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, resTypeXPath)))
    reservationTypeSelector.click()
    reservationTypeSelector.send_keys(resType[0])
    reservationTypeSelector.send_keys(Keys.ENTER)

    # TODO Duration 

    return driver

def locateSubmitButtons(drivers: dict):
    for driverName, driver in drivers.items():
        if test:
            driver['button'] = driver['driver'].find_element(By.XPATH, closeXPath)
        else:
            driver['button'] = driver['driver'].find_element(By.XPATH, submitXPath)
    if test:   
        return drivers

def prepareDrivers(drivers: dict):
    for driverName, driver in drivers.items():
        driver['driver'] = editReservation(selectReservation(selectDate(calCheck(loginDriver(driver['driver'])))))
    drivers = locateSubmitButtons(drivers)
    if test:
        return drivers

def fire(drivers: dict):
    driverView = drivers.items()
    driverList = list(driverView)
    # print(str(datetime.now()))
    for driver in driverList:
        driver[1]['button'].click()
    print('Done submitting at: ' + str(datetime.now()))
    if test:
        return drivers

def closeAllDrivers(drivers: dict):
    for driverName, driver in drivers.items():
         driver['driver'].close()



schedule.every().day.at("07:45:00", "US/Central").do(createDriverDict, numDrivers)
schedule.every().day.at("07:45:45", "US/Central").do(prepareDrivers, driverContainer)
schedule.every().day.at("07:58:00", "US/Central").do(fire, driverContainer)

while True:
    if test:
        driverDict = createDriverDict(numDrivers)
        driverDict = prepareDrivers(driverDict)
        time.sleep(10)
        print(str(datetime.now()))
        fire(driverDict)
        time.sleep(10)
        quit()
    else: 
        schedule.run_pending()
        time.sleep(1)