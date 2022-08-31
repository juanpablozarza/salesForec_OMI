
from time import sleep
from numpy import choose
import pandas as pd
from requests import head, options
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import datetime
from selenium.webdriver.common.action_chains import ActionChains


def subirArchivosSalesForce(driver, name):
    # Subir archivos a Sales force
    buttonDown = driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/section/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div/div[1]/div/div[3]/div[1]/div/div/section/div/div/div/div[1]/article/div[1]/div/div/ul/li[3]/div/div/div/div/a')
    buttonDown.click()
    sleep(1)
    importLeads = driver.find_element(By.XPATH, '/html/body/div[10]/div/ul/li[2]/a')
    importLeads.click()
    sleep(30)
    driver.switch_to.frame(driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/section/div[1]/div/div[2]/div[2]/section[1]/div/div/section/div/div[2]/div/div/div/force-aloha-page/div/iframe'))
    accountsAndLeads = driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div[2]/div[1]/div/div[2]/table/tbody/tr[3]/td/a')
    accountsAndLeads.click()
    sleep(1)
    updateAndAdd = driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div[2]/div[2]/div/div[2]/table/tbody/tr[3]/td/a')
    updateAndAdd.click()
    sleep(1)
    csvdoc=driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div[2]/div[3]/div/div[3]/a')
    csvdoc.click()
    chooseFile = driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div[2]/div[3]/div/div[3]/a/div/div[2]/form/input')
    fileToUpload = os.getcwd() + 'AMSA/CSV'+ name + '.csv'
    chooseFile.send_keys(fileToUpload)

def xlmsToCSV(path, name):
    df = pd.read_excel(path)
    pathToDownlad = os.getcwd() + 'AMSA/CSV' + name + '.csv'
    df.to_csv(pathToDownlad, index=False , header=True )

def ConnectarseSalesForce(username, password, names):
    driver = webdriver.Chrome("/Users/jpzarza/Downloads/chromedriver 3")
    driver.get(
        "https://da0000000iqpxmaw.my.salesforce.com/?ec=301&startURL=%2Fvisualforce%2Fsession%3Furl%3Dhttps%253A%252F%252Fda0000000iqpxmaw.lightning.force.com%252Flightning%252Fo%252FCampaign%252Fhome"
    )
    sleep(3)
    userField = driver.find_element(By.XPATH, '//*[@id="username"]')
    passwordField = driver.find_element(By.ID, "password")
    userField.send_keys(username)
    passwordField.send_keys(password)
    sumbit = driver.find_element(By.ID, "Login")
    sumbit.click()
    sleep(3)
    driver.get(
        "https://da0000000iqpxmaw.lightning.force.com/lightning/o/Campaign/list?filterName=Recent"
    )
    sleep(5)
    driver
    for name in names:
       searchBox = driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/section/div[1]/div[2]/div[1]/div/div/div/div/div/div/div/div[1]/div[2]/div[2]/force-list-view-manager-search-bar/div/lightning-input/div/input') 
       searchBox.click()
       sleep(3)
       searchBox.send_keys(name)
       chains = ActionChains(driver)
       chains.send_keys(Keys.ENTER)
       chains.perform()
       sleep(5)
       result = driver.find_element(By.XPATH, '//*[@id="brandBand_1"]/div/div/div/div/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/div/table/tbody/tr/th/span')
       result.click()
       sleep(5)
        # Subir archivo
       subirArchivosSalesForce(driver, name)
        # Regresar a pagina principal
       driver.get("https://da0000000iqpxmaw.lightning.force.com/lightning/o/Campaign/list?filterName=Recent")
       sleep(2)



def CrearFolder():
    date = datetime.date.today()
    cwd = os.getcwd()
    dire = "AMSA/" + "Excel"
    secondDire = 'AMSA/' + 'CSV'
    path = os.path.join(cwd, dire)
    secondPath = os.path.join(cwd, secondDire)
    os.makedirs(path)
    os.makedirs(secondPath)
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": path}
    options.add_experimental_option("prefs", prefs)
    return date, options
    # Crear folder donde se guardan los archivos


def regexNames(name):
    result = str(name[:-11] + "20" + name[-3:-1])
    return result


def InterarSeminarios(driver, date):
    names = []
    for index in range(0, 100):
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="select2-report_parameter_seminar_ominar_selector_seminar-container"]',
                )
            )
        ).click()
        sleep(1)
        chains = ActionChains(driver)
        chains.send_keys(Keys.ARROW_DOWN + Keys.ARROW_DOWN + Keys.ARROW_UP + Keys.ENTER)
        chains.perform()
        sleep(1)
        name = driver.find_element(
            By.ID, "select2-report_parameter_seminar_ominar_selector_seminar-container"
        )
        title = name.get_attribute("title")
        modified_name = regexNames(title)
        names.append(modified_name)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="report_parameter_seminar_ominar_selector"]/div[2]/span',
                )
            )
        ).click()
        chains.send_keys(Keys.ENTER)
        sleep(1)
        chains.perform()
        search = driver.find_element(By.XPATH, '//*[@id="button-area"]/a[1]')
        search.click()
        download = driver.find_element(By.XPATH, '//*[@id="button-area"]/button')
        sleep(5)
        download.click()
        sleep(3)
        cwd = os.getcwd()
        old_path = cwd + "/AMSA/" + str(date) + "/participants-list.xlsx"
        new_path = cwd + "/AMSA/" + str(date) + "/" + str(modified_name) + ".xlsx"
        os.rename(old_path, new_path)
        xlmsToCSV(new_path,str(modified_name))
    return names


# Interar por cada seminario y bajar los archivos
def connectOMI(omiUser, omiPassword, options):
    driver = webdriver.Chrome(
        "/Users/jpzarza/Downloads/chromedriver 3", options=options
    )
    driver.get("https://portal.openmedicalinstitute.org/login")
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    username.send_keys(omiUser)
    password.send_keys(omiPassword)
    submit = driver.find_element(By.ID, "_submit")
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
    omiUser = os.getenv("USERNAME_OMI")
    omiPassword = os.getenv("PASSWORD_OMI")
    salesforceUsername = os.getenv("USERNAME_SALESFORCE")
    salesforcePassword = os.getenv("PASSWORD_SALESFORCE")
    date, options = CrearFolder()
    # driver = connectOMI(omiUser, omiPassword, options)
    # titulos = InterarSeminarios(driver, date)
    # ConnectarseSalesForce(salesforceUsername, salesforcePassword, ['Medical Leadership 2023', 'Anesthesiology and Intensive Care 2023', 'ESU Master Class in Urology 2023'])
    # clearFolder(date)


main()
