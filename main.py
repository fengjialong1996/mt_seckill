from selenium import webdriver
from selenium.webdriver.remote import webelement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import datetime
import time
import logging
from common.constant import platform2act_pwd, platform2url, platform2start_timestamp

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-8s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class ChromeDriver():
    """
    初始化Chrome driver
    """

    def __init__(self, executable_path="D:\Application\chromedriver_win32\chromedriver.exe"):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument("--disable-blink-features=AutomationControlled")
        #options.add_argument('--headless')  # 浏览器不提供可视化页面，打开选项不会打开浏览器
        #options.add_argument('blink-settings=imagesEnabled=false')  #是否加载图片，打开不会加载图片
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["pageLoadStrategy"] = "none"
        prefs={"":""} #禁止弹窗
        prefs["credentials_enable_service"] = False  
        prefs["profile.password_manager_enabled"] = False
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(executable_path=executable_path, options=options)

def login_tianmao(driver):
    driver.get(platform2url["tianmao"]["login_url"])
    driver.switch_to.frame(driver.find_element(by=By.ID, value='J_loginIframe'))
    driver.find_element(by=By.ID, value='fm-login-id').send_keys(platform2act_pwd["tianmao"]["account"])
    driver.find_element(by=By.ID, value='fm-login-password').send_keys(platform2act_pwd["tianmao"]["password"])
    driver.find_element(by=By.CLASS_NAME, value='fm-btn').click()
    # tianmao_unlock(driver)
    while 'login' in driver.current_url:
        print(driver.current_url)
        time.sleep(1)
    logger.info("login in tianmao successfully")

def login(driver, platform):
    match platform:
        case "tianmao":
            login_tianmao(driver)
        case _:
            print("input platform error")

def tianmao_unlock(driver: webdriver.Chrome):
    """
    execute moving block
    """
    # try:
    print("move the block...")
    # WebDriverWait(driver, 6).until(
    #     EC.presence_of_element_located((By.ID, "#baxia-dialog-content"))
    # )
    time.sleep(6)
    driver.switch_to.frame(driver.find_element(by=By.ID, value="baxia-dialog-content"))
    # WebDriverWait(driver,2).until(
    #     EC.frame_to_be_available_and_switch_to_it((By.ID,"#baxia-dialog-content"))
    # )
    bar_element = driver.find_element(by=By.CLASS_NAME, value='nc-lang-cnt')
    print("11111")
    slider_width = bar_element.size["width"]
    slider_height = bar_element.size["height"]
    slider_x = bar_element.location["x"]
    slider_y = bar_element.location["y"]
    print("slider_width:", slider_width)
    move_distance = slider_width - 100
    actions = ActionChains(driver)
    actions.move_to_element(bar_element).perform()
    actions.drag_and_drop_by_offset(bar_element, move_distance, 0).perform()
    print("bar_element:", bar_element)
    time.sleep(0.5)
    # except Exception as e:
    #     print(u"move the block failed!!! Error: %s" % e)
    # if driver.find_element(by=By.CLASS_NAME, value='nc-lang-cnt'):
    #     tianmao_unlock(driver)

if __name__ == '__main__':
    # 1. init browser driver
    chrome_driver = ChromeDriver().driver
    # 2. open browser and login in
    print("opening browser and logining in")
    login(driver=chrome_driver, platform="tianmao")
    
    # 3. open maitai page
    chrome_driver.get(platform2url["tianmao"]["maotai_url"])
    
    # 4. buy on time
    buy_button_element = chrome_driver.find_element(by=By.CSS_SELECTOR, value="[class*=Actions--leftButtons]")
    buy_button_element_text = buy_button_element.text
    while True:
        current_timestamp = int(time.time() * 1000)
        if platform2start_timestamp["tianmao"] > current_timestamp > platform2start_timestamp["tianmao"] - 300000:
            logger.info("Nowtime: {}, Timestamp:{}. seckill will start in about 3 min".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(time.time() * 1000)))
            print("buy_button_element_text:", type(buy_button_element_text), buy_button_element_text)
            WebDriverWait(chrome_driver, 6).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[class*=Actions--leftButtons]"), "即将开始，03.24 20:00开售")
            )
            WebDriverWait(chrome_driver, 360).until_not(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[class*=Actions--leftButtons]"), "即将开始，03.24 20:00开售")
            )
            buy_button_element = chrome_driver.find_element(by=By.CSS_SELECTOR, value="[class*=Actions--leftButtons]")
            buy_button_element_text = buy_button_element.text
            print("buy_button_element_text:", type(buy_button_element_text), buy_button_element_text)
            logger.info("Nowtime: {}, Timestamp:{}. seckill is starting".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(time.time() * 1000)))
            try:
                for i in range(10):
                    buy_button_element.click()
                    print("botton clicked")
                    time.sleep(0.2)
                while True:
                    if 'detail' not in chrome_driver.current_url:
                        continue
            except NoSuchElementException:
                print("click botton failed")
        else:
            logger.warning("Nowtime: {}, Timestamp:{}. Please check the time!!!".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(time.time() * 1000)))
    print("closing browser")

