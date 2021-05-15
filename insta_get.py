from selenium import webdriver
import time, pickle, os
from config import insta_login, insta_pass

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_argument("--mute-audio")
# driver = webdriver.Chrome(executable_path=r"drivers/chromedriver.exe", options=chrome_options)


driver.get(url=r"https://www.instagram.com")
driver.implicitly_wait(3)
for cookie in pickle.load(open(f"login.cookies", "rb")):
    driver.add_cookie(cookie)
driver.implicitly_wait(2)
driver.refresh()
print("ishga tayyor !")


def get_data(url):
    driver.get(url=url)
    # driver.implicitly_wait(2)
    return driver.find_element_by_tag_name("pre").get_attribute('innerText')
    # return driver.page_source


def login():
    try:
        print("Dastur ishga tushdi !")
        driver.get(url=r"https://www.instagram.com")
        driver.implicitly_wait(3)
        driver.find_element_by_name("username").send_keys(insta_login)
        time.sleep(1)
        driver.find_element_by_name("password").send_keys(insta_pass)
        time.sleep(1)
        driver.find_element_by_css_selector('button[type="submit"]').click()
        time.sleep(3)
        print("Akkountdamiz !")
        pickle.dump(driver.get_cookies(), open(f"login.cookies", "wb"))
        print("Login malumotlari saqlandi !")
    except Exception as ex:
        print('Nimadur xato !')
        print(ex)
        driver.close()
        driver.quit()
        print('Dastur tugatildi !')


def driver_down():
    driver.close()
    driver.quit()
    print('Dastur tugatildi !')


if __name__ == '__main__':
    login()
