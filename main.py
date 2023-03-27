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
import threading
from common.constant import platform2act_pwd, platform2url, platform2start_timestamp

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(threadName)-14s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


browser_type2execute_path = {
    "Chrome": "D:\chromedriver.exe",
    "Edge": "D:\msedgedriver.exe"
}

browser_type2option = {
    "Chrome": webdriver.ChromeOptions,
    "Edge": webdriver.EdgeOptions
}

browser_type2desired_capabilities = {
    "Chrome": DesiredCapabilities.CHROME,
    "Edge": DesiredCapabilities.EDGE
}

browser_type2browser = {
    "Chrome": webdriver.Chrome,
    "Edge": webdriver.Edge
}

class Driver():
    "初始化一个driver"
    def __init__(self, browser_type: str) -> None:
        options = browser_type2option[browser_type]()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument("--disable-blink-features=AutomationControlled")
        #options.add_argument('--headless')  # 浏览器不提供可视化页面，打开选项不会打开浏览器
        #options.add_argument('blink-settings=imagesEnabled=false')  #是否加载图片，打开不会加载图片
        desired_capabilities = browser_type2desired_capabilities[browser_type]
        desired_capabilities["pageLoadStrategy"] = "none"
        prefs={"":""} #禁止弹窗
        prefs["credentials_enable_service"] = False  
        prefs["profile.password_manager_enabled"] = False
        options.add_experimental_option('prefs', prefs)
        self.driver = browser_type2browser[browser_type](executable_path=browser_type2execute_path[browser_type], options=options)

def login_tianmao(driver: Driver, acc_pwd: dict) -> None:
    """
    login in tianmao
    
    param driver: Driver, web driver
    param acc_pwd: dict, {"account": [account], "password": [password]} in constant.platform2act_pwd.value
    """
    driver.get(platform2url["tianmao"]["login_url"])
    driver.switch_to.frame(driver.find_element(by=By.ID, value='J_loginIframe'))
    driver.find_element(by=By.ID, value='fm-login-id').send_keys(acc_pwd["account"])
    driver.find_element(by=By.ID, value='fm-login-password').send_keys(acc_pwd["password"])
    driver.find_element(by=By.CLASS_NAME, value='fm-btn').click()
    # tianmao_unlock(driver)
    while 'login' in driver.current_url:
        # print(driver.current_url)
        time.sleep(1)
    logger.info("login in tianmao successfully")

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

def run(browser_type: str, acc_pwd: dict) -> None:
    # 1. init browser driver
    web_driver = Driver(browser_type).driver
    # 2. open browser and login in
    logging.info("opening browser and logining in")
    login_tianmao(driver=web_driver, acc_pwd=acc_pwd)
    # 3. open maitai page
    web_driver.get(platform2url["tianmao"]["maotai_url"])
    # 4. buy on time
    date_str = datetime.datetime.now().strftime("%m.%d")
    before_text = "即将开始，{} 20:00开售".format(date_str)
    current_timestamp = int(time.time() * 1000)
    while True:
        if platform2start_timestamp["tianmao"] > current_timestamp > platform2start_timestamp["tianmao"] - 7200000:
            logging.info("Nowtime: {}, Timestamp: {}. seckill will start soon".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(time.time() * 1000)))
            WebDriverWait(web_driver, 6).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[class*=Actions--leftButtons]"), before_text)
            )
            buy_button_element_text = web_driver.find_element(by=By.CSS_SELECTOR, value="[class*=Actions--leftButtons]").text
            logging.info("buy_button_element_text: {}".format(buy_button_element_text))
            WebDriverWait(web_driver, 7200).until_not(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[class*=Actions--leftButtons]"), before_text)
            )
            buy_button_element = web_driver.find_element(by=By.CSS_SELECTOR, value="[class*=Actions--leftButtons]")
            buy_button_element_text = buy_button_element.text
            logging.info("buy_button_element_text: {}".format(buy_button_element_text))
            logging.info("Nowtime: {}, Timestamp: {}. seckill is starting".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(time.time() * 1000)))
            try:
                for i in range(10):
                    buy_button_element.click()
                    print("buy-botton clicked!")
                    logging.info("buy-botton clicked!")
                    time.sleep(0.2)
                while True:
                    if 'detail' not in web_driver.current_url:
                        continue
            except NoSuchElementException:
                print("click buy-botton failed!")
                logging.info("click buy-botton failed!")
        else:
            logger.warning("Nowtime: {}, Timestamp: {}. Please check the time!!!".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(time.time() * 1000)))
    print("over")

if __name__ == '__main__':
    t1 = threading.Thread(target=run, name="Thread-Chrome", args=("Chrome", platform2act_pwd["tianmao_acc1"]))
    t2 = threading.Thread(target=run, name="Thread-Edge", args=("Edge", platform2act_pwd["tianmao_acc2"]))
    t1.start()
    t2.start()