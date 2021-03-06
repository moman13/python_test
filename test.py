from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from faker import Faker
file = open('proxies.txt')
Lines = file.readlines()
output = open('output.txt','a')
for line in Lines:
    try:
        option = webdriver.ChromeOptions()
        option.add_argument('proxy-server='+line)
        EXE_PATH = r'C:\chromedriver.exe'
        driver = webdriver.Chrome(executable_path=EXE_PATH,options=option)
        driver.get('https://fast.com/ar/')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'language-selector-container')))
        output.write(line)
        output.write('\n')
        print(line)
        driver.quit()
    except TimeoutException as ex:
        print "It is all good, no element there"
        driver.quit()
    except  WebDriverException as ex:
        print "bad Proxy"
        driver.quit()