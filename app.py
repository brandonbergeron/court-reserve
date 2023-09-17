import time
from datetime import datetime
import schedule
import questionary
from utils.maps import courtMap, weekdayTimeMap, saturdayTimeMap, sundayTimeMap, days, months, dates
from utils.creds import userName, password
from utils.paths import loginPage, reservationUrl, closeXPath, submitXPath, resTypeXPath
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


mmDD = str(datetime.now().date())[-5:]
yyyy = str(datetime.now().date())[:4]

newYear = ['12-25', '12-26', '12-27', '12-28', '12-29', '12-30', '12-31']
targetYear = yyyy

if str(datetime.now().date())[-5:] in newYear: # TODO check this
    targetYear = str(int(yyyy) + 1)

test = input('Are you running in test mode? (y/n): ').lower().strip() == 'y'
numDrivers = int(questionary.text('How many browsers to boot up?').ask())
day = questionary.select(
     "Day: ",
     choices = days,
).ask()
targetMonth = questionary.select(
     "Month:",
     choices = months).ask()
targetDate = questionary.select(
     "Date:",
     choices = dates,
     default = str(datetime.now().day)
)
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


def calCheck(driver: webdriver):
    nextButtonClassName = "k-nav-next"
    monthYearClassName = "k-nav-fast"

    datePicker = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".k-icon.k-i-calendar")))
    datePicker.click()

    selectedYear = driver.find_element(By.CLASS_NAME, monthYearClassName)
    selectedMonthYearString = selectedYear.get_attribute("innerHTML")
    targetMonthYearString = targetMonth + ' ' + targetYear
    print(selectedMonthYearString)

    while (selectedMonthYearString != targetMonthYearString):
            next_click = driver.find_element(By.CLASS_NAME, nextButtonClassName)
            next_click.click()
            time.sleep(2)

            selectedYear = driver.find_element(By.CLASS_NAME, monthYearClassName)
            selectedMonthYearString = selectedYear.get_attribute("innerHTML")
            # print(selected_month_year_string)


def selectDate(driver: webdriver):
    calTable = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "k-content")))

    for row in calTable.find_elements(By.XPATH, "//tr"):
                for cell in row.find_elements(By.XPATH, "td"):
                    if (cell.text == targetDate):
                        driver.find_element(By.LINK_TEXT, targetDate).click()
                        time.sleep(4)
                        return driver
                    
timeSlotXPath = f"/html/body/div[1]/div[2]/div/div[2]/div/div/div/div/div/div/div/div/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[{days[day][targetTime]}]/td[{courtMap[targetCourt]}]/span/button"

def selectReservation(driver: webdriver):
    reservationSlot = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, timeSlotXPath)))
    reservationSlot.click()
    time.sleep(2)

    return driver

def editReservation(driver: webdriver):
     # TODO this is hardcoded for Singles reservations but should be input driven
    reservationTypeSelector = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, resTypeXPath)))
    reservationTypeSelector.click()
    reservationTypeSelector.send_keys(resType[0])
    reservationTypeSelector.send_keys(Keys.ENTER)

    # TODO add ability to select duration/add guests? 

    return driver

def locateSubmitButtons(drivers: dict):
    for driverName, driver in drivers.items():
        if test:
            driver['button'] = driver['driver'].find_element(By.XPATH, closeXPath)
        else:
            driver['button'] = driver['driver'].find_element(By.XPATH, submitXPath)
        
    return drivers

def prepareDrivers(drivers: dict):
    for driverName, driver in drivers.items():
        driver['driver'] = loginDriver(driver['driver'])
        driver['driver'] = calCheck(driver['driver'])
        driver['driver'] = selectDate(driver['driver'])
        driver['driver'] = selectReservation(driver['driver'])
        driver['driver'] = editReservation(driver['driver'])
        # driver = locateSubmitButton(driver)
        # driver = selectReservation(selectDate(initDriver(driver)))  This is cool but reservation type gets fucked up
    drivers = locateSubmitButtons(drivers)

    return drivers

# some_dict_view = some_dict.items()
# some_list = list(some_dict_view)

def fire(drivers: dict):
    driverView = drivers.items()
    driverList = list(driverView)
    # print(str(datetime.now()))
    for driver in driverList:
        driver[1]['button'].click()
    # for driverName, driver in drivers.items():
    #     driver['button'].click()
    #     #   time.sleep(.05)
    print(str(datetime.now()))
    # return drivers

def closeAllDrivers(drivers: dict):
    for driverName, driver in drivers.items():
         driver['driver'].close()



# schedule.every().day.at("09:24:00", "US/Central").do(createDriverDict, numDrivers)
# schedule.every().day.at("09:25:30", "US/Central").do(prepareDrivers, driverContainer)
# schedule.every().day.at("09:34:58", "US/Central").do(fire, driverContainer)

while True:
    if test:
        driverDict = createDriverDict(numDrivers)
        driverDict = prepareDrivers(driverDict)
        time.sleep(10)
        print(str(datetime.now()))
        fire(driverDict)
        quit()
    else: 
        schedule.run_pending()
        time.sleep(1)