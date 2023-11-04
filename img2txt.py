import requests
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from datetime import datetime
import settings
from AI_model import ai_model
from cleaning import clean_text
from compare__pics import compare_images
from OCR import ocr
import pandas as pd
import os
import threading
import queue
def start_convert(gui_queue,stop_event):
        cookies = "D:/STUDIES/python/messenger_API/test1/mine/cookies"
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir=" + cookies)
        driver = webdriver.Chrome('chromedriver.exe', options=options)
        csv_filename = "data.csv"
        if not os.path.exists(csv_filename):
            df = pd.DataFrame(columns=['Name', 'Text', 'Timestamp'])
            df.to_csv(csv_filename, index=False)
        df = pd.read_csv(csv_filename)
        print("Opening Chrome")
        print("Starting Log in....")
        test=os.environ.get('test')

        driver.get('https://www.messenger.com/')
        sleep(3)
        login_form_present = len(driver.find_elements(By.XPATH, '//*[@id="email"]')) > 0
        if login_form_present:
            driver.find_element_by_xpath('//*[@id="email"]').send_keys(settings.username_email)
            # driver.find_element(by=By.XPATH, value='//*[@id="email"]')    #new one
            driver.find_element_by_xpath('//*[@id="pass"]').send_keys(settings.password)
            driver.find_element_by_xpath('//input[@class="_2qcs"]/..').click()
            driver.find_element_by_xpath('//*[@id="loginbutton"]').click()
            print("Waiting for a few seconds...")
            sleep(1)
            if driver.find_element_by_xpath('//*[@id="XMessengerDotComLoginViewPlaceholder"]'): print("waiting for auth")
            wait = WebDriverWait(driver, 99999)
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Conversation information"]')))
        else:
            print("You are already connected.")
        # Finds users in DM list
        while not stop_event.is_set():
            for conversation_namee in settings.conversation_name:
                wait = WebDriverWait(driver, 9999)
                wait.until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Conversation information"]')))
                element = driver.find_element(By.XPATH, '//div[@aria-label="Conversation information"]')
                try:
                    driver.find_element(By.XPATH, '//span[contains(text(), "Media, files and links")]')
                    driver.find_element(By.XPATH, '//span[contains(text(), "Media, files")]')
                except NoSuchElementException:
                    element.click()
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "x1lliihq")))
                elements = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, ".x1lliihq.x193iq5w.x6ikm8r.x10wlt62.xlyipyv.xuxw1ft")))
                print(conversation_namee)
                for element3 in elements:
                    text = element3.text
                    if text == conversation_namee:
                        break
                    # else:
                    #     driver.refresh()
                    #     i += 1
                    #     if i == 6: print("user name not found");conversation_namee += 1;
                    #     continue
                try:
                    element3.click()
                except StaleElementReferenceException:
                    element = driver.find_element(By.CSS_SELECTOR, ".x1lliihq.x193iq5w.x6ikm8r.x10wlt62.xlyipyv.xuxw1ft")
                    element.click()
                # click on the last picture
                try:
                    driver.find_element(By.XPATH,
                                        '//div[contains(@class, "x78zum5 x1q0g3np x1a02dak x1kgmq87 xwrv7xz xmgb6t1 x8182xy")]')
                except NoSuchElementException:
                    try:
                        sleep(1);driver.find_element(By.XPATH, '//span[contains(@class, "x193iq5w") and text()="Media"]')
                    except NoSuchElementException:
                        sleep(1)
                        driver.find_element(By.XPATH, '//span[starts-with(text(), "Media, files")]').click()
                    wait.until(
                        EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "x193iq5w") and text()="Media"]')))
                    driver.find_element(By.XPATH, '//span[contains(@class, "x193iq5w") and text()="Media"]').click()
                parent_div = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//div[contains(@class, "x78zum5 x1q0g3np x1a02dak x1kgmq87 xwrv7xz xmgb6t1 x8182xy")]')))
                if parent_div:
                    # Find the first image element within the parent div
                    first_image = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Open photo"]')))
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Open photo"]')))
                    first_image.click()
                    wait.until(EC.presence_of_element_located((By.XPATH, '//img[@class="x4ju7c5 xt7dq6l x193iq5w x14atkfc"]')))
                    # Get the image element
                    img_element = driver.find_element(By.XPATH, '//img[@class="x4ju7c5 xt7dq6l x193iq5w x14atkfc"]')
                    # Get the image URL and download it
                    image_url = img_element.get_attribute('src')
                    if os.path.exists('pics/' + conversation_namee + '.jpg'):
                        local_filename = 'pics/' + conversation_namee + 'new.jpg'
                    else:
                        local_filename = 'pics/' + conversation_namee + '.jpg'
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        with open(local_filename, 'wb') as f:
                            f.write(response.content)
                        print(f"Image downloaded and saved as {local_filename}")
                    #compare last photo and new photo and process the new photo
                    if not compare_images("pics/" + conversation_namee + "new.jpg", "pics/" + conversation_namee + ".jpg"):
                        text1 = ocr(local_filename);text1=clean_text(text1)
                        text2 = ai_model(local_filename);text2=clean_text(text2)
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        new_row = [conversation_namee,text1+text2, timestamp]
                        gui_queue.put(new_row)
                        new_row_df = pd.DataFrame([new_row], columns=df.columns)
                        df = pd.concat([df, new_row_df], ignore_index=True)
                        df.to_csv(csv_filename, index=False)
                    os.remove('pics/' + conversation_namee + '.jpg')
                    os.rename('pics/' + conversation_namee + 'new.jpg','pics/' + conversation_namee + '.jpg')
                driver.get('https://www.messenger.com/')
        driver.close()