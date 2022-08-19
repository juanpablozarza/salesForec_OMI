
from json import load
from time import sleep
from dotenv.main import load_dotenv
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import os
import datetime
from selenium.webdriver.common.action_chains import ActionChains


def SubirArchivosSalesForce():
    # Subir archivos a Sales force
    pass


def ConnectarseSalesForce():
    driver = webdriver.Chrome('/Users/jpzarza/Downloads/chromedriver')
    driver.get('https://da0000000iqpxmaw.my.salesforce.com/?ec=301&startURL=%2Fvisualforce%2Fsession%3Furl%3Dhttps%253A%252F%252Fda0000000iqpxmaw.lightning.force.com%252Flightning%252Fo%252FCampaign%252Fhome')
    # Connectarse a la pagina de sales force
    pass


def CrearFolder():
    date = datetime.date.today()
    os.mkdir("AMSA/" + date + "")
    return date
    # Crear folder donde se guardan los archivos
    pass


def InterarSeminarios(driver): 
   for index in range(0,100):
     WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="select2-report_parameter_seminar_ominar_selector_seminar-container"]'))).click()
     sleep(3)
     chains = ActionChains(driver)
     chains.send_keys(Keys.ARROW_DOWN + Keys.ENTER)
     chains.perform()
     WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="report_parameter_seminar_ominar_selector"]/div[2]/span/span[1]/span'))).click()
     chains.send_keys(Keys.ARROW_DOWN + Keys.ENTER)
     sleep(2)
        

# Interar por cada seminario y bajar los archivos
def connectOMI(username, password):
    driver = webdriver.Chrome('/Users/jpzarza/Downloads/chromedriver 3')
    driver.get("https://portal.openmedicalinstitute.org/login")
    username = driver.find_element(By.ID,"username")
    password = driver.find_element(By.ID, "password")
    username.send_keys(username)
    password.send_keys(password)
    submit = driver.find_element(By.ID,"_submit")
    submit.click()
    driver.get("https://portal.openmedicalinstitute.org/report/loc_participant_list")
    sleep(10)
    return driver
    # Connectarse a la pagina y navergar a los seminarios


def clearFolder(date):
    os.rmdir("AMSA/" + date + "")
    # Destruir folder


def main():
 load_dotenv()   
 omiUser = os.environ['USERNAME_OMI']
 omiPassword = os.environ['PASSWORD_OMI']
 driver = connectOMI(omiUser, omiPassword)
 InterarSeminarios(driver)
    


main()
