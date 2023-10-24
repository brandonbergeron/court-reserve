import time
from datetime import datetime, timedelta
import schedule
import questionary
import threading
from utils.maps import courtMap, durationMap, days, months
from utils.localcreds import loginPage, reservationUrl, userName, password
from utils.paths import closeXPath, submitXPath, resTypeXPath, resDurationXPath
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def getTargetDate():
    now = datetime.now()
    
    if now.time() < datetime.now().replace(hour=8, minute=0, second=0, microsecond=0).time():
        startDay = now.replace(hour=8, minute=0, second=0, microsecond=0)
    else:
        startDay = now + timedelta(days=1)
        startDay = startDay.replace(hour=8, minute=0, second=0, microsecond=0)
    
    resTarget = startDay + timedelta(days=7)
    
    dayOfWeek = resTarget.strftime('%A')
    month = resTarget.strftime('%B')
    targetDate = str(resTarget.day)

    return dayOfWeek, month, targetDate

targetDay, targetMonth, targetDate = getTargetDate()
submit = input("Would you like to make a scheduled reservation? (y/n): ").lower().strip() == "y"

if not submit:
    numDrivers = int(questionary.text("How many browsers to boot up?").ask())
else:
    numDrivers = 20

targetCourt = questionary.select("Select a court: ", choices=courtMap.keys()).ask()
targetTime = questionary.select("Select a time: ", choices=days[targetDay].keys()).ask()
resType = "Singles"
resDuration = questionary.select("Duration: ", choices=durationMap.keys()).ask()
courtXPath = f"/html/body/div[1]/div[2]/div/div[2]/div/div/div/div/div/div/div/div/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[{days[targetDay][targetTime]}]/td[{courtMap[targetCourt]}]/span/button"

driverContainer = {}

def createDriverDict(numDrivers: int):
    global driverContainer

    for i in range(numDrivers):
        driverContainer[f"driver{i}"] = {
            "driver": webdriver.Chrome(),
            "button": None,
        }

    return driverContainer


def loginDriver(driver: webdriver):
    driver.get(loginPage)
    userNameField = driver.find_element(By.NAME, "UserNameOrEmail")
    passwordField = driver.find_element(By.NAME, "Password")
    userNameField.send_keys(userName)
    passwordField.send_keys(password)
    loginButton = driver.find_element(By.CLASS_NAME, "btn-log")
    loginButton.click()
    time.sleep(2)
    driver.get(reservationUrl)
    time.sleep(4)

    return driver


# Check for if desired date is not in current month
def calCheck(driver: webdriver):
    datePicker = driver.find_element(By.CSS_SELECTOR, ".k-icon.k-i-calendar")
    datePicker.click()
    time.sleep(2)

    currentMonth = str(datetime.now().date())[-5:-3]

    if targetMonth != months[currentMonth[:2]]:
        nextButton = driver.find_element(By.CSS_SELECTOR, "[data-action='next']")
        nextButton.click()
        time.sleep(2)

    return driver


# Find date in calendar popup
def selectDate(driver: webdriver):
    calTable = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "k-content"))
    )

    for row in calTable.find_elements(By.XPATH, "//tr"):
        for cell in row.find_elements(By.XPATH, "td"):
            if cell.text == targetDate:
                dateElem = driver.find_element(By.LINK_TEXT, targetDate)
                dateElem.click()
                time.sleep(3)
                return driver
            

def selectReservation(driver: webdriver, driverId):
    
    reservationSlot = driver.find_element(By.XPATH, courtXPath)
    reservationSlot.click()

    return driver


def editReservation(driver: webdriver):
    # Singles, Doubles, or Ball Machine:
    reservationTypeSelector = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, resTypeXPath))
    )
    reservationTypeSelector.click()
    reservationTypeSelector.send_keys(resType[0])
    reservationTypeSelector.send_keys(Keys.ENTER)

    time.sleep(2)

    reservationDurationSelector = driver.find_element(By.XPATH, resDurationXPath)
    reservationDurationSelector.click()
    time.sleep(1)
    reservationDurationSelector.send_keys(durationMap[resDuration])
    time.sleep(1)
    reservationDurationSelector.send_keys(Keys.ENTER)

    # TODO Duration

    return driver

def locateSubmitButtons(drivers: dict):
    for driverId in list(drivers.keys()):  # Iterate over a copy of the keys
        try:
            driverInstance = drivers[driverId]["driver"]

            if not submit:
                drivers[driverId]["button"] = driverInstance.find_element(By.XPATH, closeXPath)
            else:
                drivers[driverId]["button"] = driverInstance.find_element(By.XPATH, submitXPath)

        except NoSuchElementException as e:
            # Handle specific exceptions for missing elements
            print(f"Error locating element for {driverId}: {e}")
            driverInstance.quit()
            del drivers[driverId]
        except Exception as e:
            # Handle other unexpected exceptions
            print(f"Unexpected error with {driverId}: {e}")
            driverInstance.quit()
            del drivers[driverId]

    if not submit:
        return drivers

def prepareDrivers(drivers: dict):
    for driverId in list(drivers.keys()):  # Iterate over a copy of the keys
        try:
            driverInstance = drivers[driverId]["driver"]

            driverInstance = loginDriver(driverInstance)
            driverInstance = calCheck(driverInstance)
            driverInstance = selectDate(driverInstance)
            driverInstance = selectReservation(driverInstance, driverId)
            driverInstance = editReservation(driverInstance)

            drivers[driverId]["driver"] = driverInstance

        except Exception as e:
            # If an exception occurs at any stage
            print(f"Removing {driverId} due to error: {e}")
            driverInstance.quit()
            del drivers[driverId]
    
    drivers = locateSubmitButtons(drivers)

    if not submit:
        return drivers


def click_button(driver_and_button):
    driver_and_button["button"].click()


def fire(drivers: dict):
    threads = []
    time.sleep(.8)

    for driver_and_button in drivers.values():
        thread = threading.Thread(target=click_button, args=(driver_and_button,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("Done submitting at: " + str(datetime.now()))
    if not submit:
        return drivers


def closeAllDrivers(drivers: dict):
    for driver in drivers.values():
        driver["driver"].close()


schedule.every().day.at("08:40:00", "US/Eastern").do(createDriverDict, numDrivers)
schedule.every().day.at("08:41:30", "US/Eastern").do(prepareDrivers, driverContainer)
schedule.every().day.at("08:59:55", "US/Eastern").do(fire, driverContainer)
schedule.every().day.at("09:30:00", "US/Eastern").do(closeAllDrivers, driverContainer)



while True:
    if not submit:
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
