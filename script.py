import urllib
from time import sleep

from requests import options
from dotenv import load_dotenv
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


def ConnectarseSalesForce(username, password):
    driver = webdriver.Chrome('/Users/jpzarza/Downloads/chromedriver')
    driver.get('https://da0000000iqpxmaw.my.salesforce.com/?ec=301&startURL=%2Fvisualforce%2Fsession%3Furl%3Dhttps%253A%252F%252Fda0000000iqpxmaw.lightning.force.com%252Flightning%252Fo%252FCampaign%252Fhome')
    username = driver.find_element(By.XPATH, '//*[@id="username"]')
    password = driver.find_element(By.XPATH, '//*[@id="password"]')
    username.send_keys(username)
    password.send_keys(password)
    sumbit = driver.find_element(By.ID, 'Login')
    sumbit.click()
    sleep(3)
    driver.get('https://da0000000iqpxmaw.lightning.force.com/lightning/o/Campaign/list?filterName=Recent')
    campaings =  driver.find_element(By.XPATH, '//*[@id="brandBand_1"]/div/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/div/table/tbody')
    seminarios = os.listdir()
    for i in campaings:
        for seminario in seminarios:
            if(i.text == seminario):
                pass 
                # Pasar a importar
    # Connectarse a la pagina de sales force
    


def CrearFolder():
    date = datetime.date.today()
    cwd = os.getcwd()
    dire = "AMSA/" + str(date) + ""
    path = os.path.join(cwd , dire )
    os.makedirs(path)
    options = webdriver.ChromeOptions() ;
    prefs = {"download.default_directory" : path } 
    options.add_experimental_option("prefs",prefs);
    return date, options
    # Crear folder donde se guardan los archivos


def InterarSeminarios(driver, date): 
   names = [] 
   for index in range(0,100):
     WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="select2-report_parameter_seminar_ominar_selector_seminar-container"]'))).click()
     sleep(1)
     chains = ActionChains(driver)
     chains.send_keys(Keys.ARROW_DOWN +Keys.ARROW_DOWN + Keys.ARROW_UP + Keys.ENTER)
     chains.perform()
     sleep(1)
     name = driver.find_element(By.ID, 'select2-report_parameter_seminar_ominar_selector_seminar-container')
     title = name.get_attribute('title')
     names.append(title)
     WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="report_parameter_seminar_ominar_selector"]/div[2]/span'))).click()
     chains.send_keys( Keys.ENTER)
     sleep(1)
     chains.perform()
     search = driver.find_element(By.XPATH, '//*[@id="button-area"]/a[1]')
     search.click()
     download = driver.find_element(By.XPATH, '//*[@id="button-area"]/button')
     sleep(5)
     download.click()
     sleep(3)
     cwd = os.getcwd()
     
     if(index == 0):
         old_path = cwd + '/AMSA/' + str(date) + '/participants-list.xlsx'
     else: 
         old_path = cwd+ '/AMSA/'+ str(date) + '/participants-list('+ str(index)+ ').xlsx'
     new_path = cwd + '/AMSA/'+ str(date) + '/'+str(title) +'.xlsx'
     os.rename(old_path, new_path)
   return names;
        

# Interar por cada seminario y bajar los archivos
def connectOMI(omiUser, omiPassword, options):
    driver = webdriver.Chrome('/Users/jpzarza/Downloads/chromedriver 3', options= options)
    driver.get("https://portal.openmedicalinstitute.org/login")
    username = driver.find_element(By.ID,"username")
    password = driver.find_element(By.ID, "password")
    username.send_keys(omiUser)
    password.send_keys(omiPassword)
    submit = driver.find_element(By.ID,"_submit")
    submit.click()
    driver.get("https://portal.openmedicalinstitute.org/report/loc_participant_list")
    sleep(10)
    return driver
    # Connectarse a la pagina y navergar a los seminarios


def clearFolder(date):
    os.removedirs("AMSA/" + date + "")
    # Destruir folder


def main():
 load_dotenv()   
 omiUser = os.getenv('USERNAME_OMI')
 omiPassword = os.getenv('PASSWORD_OMI')
 salesforceUsername = os.getenv('USERNAME_SALESFORCE')
 salesforcePassword = os.getenv('PASSWORD_SALESFORCE')
 date, options = CrearFolder()
 driver = connectOMI(omiUser, omiPassword, options)
 titulos = InterarSeminarios(driver, date)
 ConnectarseSalesForce(salesforceUsername, salesforcePassword)
 clearFolder(date)


main()
