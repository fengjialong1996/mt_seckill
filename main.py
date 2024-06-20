from selenium import webdriver
from selenium.webdriver.remote import webelement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.service import Service

import datetime
import time
import logging
import requests
import threading
from common.constant import platform2act_pwd, platform2url, platform2start_timestamp
from common.common import MyService

logger = logging.getLogger()
handler_1 = logging.StreamHandler()
log_file = "./log/{}.log".format(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
handler_2 = logging.FileHandler(filename=log_file, encoding="utf-8")
formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(threadName)-14s %(message)s")
handler_1.setFormatter(formatter)
handler_2.setFormatter(formatter)
# logger.addHandler(handler_1)
logger.addHandler(handler_2)
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
        # self.service = MyService(executable=browser_type2execute_path[browser_type])
        # self.driver = browser_type2browser[browser_type](service=self.service, options=options)
        self.driver = webdriver.Chrome(service=webdriver)

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

def get_current_timestamp() -> None:
    current_timestamp = int(time.time() * 1000)
    return current_timestamp

def get_server_time() -> tuple:
    res = requests.head(platform2url["tianmao"]["maotai_cart_url"])
    server_time = res.headers["Date"]
    logging.info("server_time:{}".format(server_time))
    # print("current_time:{}".format(datetime.datetime.now()))
    # print("server_time:{}".format(server_time))
    server_time_stamp = time.mktime(time.strptime(server_time, '%a, %d %b %Y %H:%M:%S %Z')) * 1000
    # delta_timestamp = get_current_timestamp() - server_time_stamp - 8*60*60*1000
    # print("get_current_timestamp():{}".format(get_current_timestamp()))
    # print("server_time_stamp:{}".format(server_time_stamp))
    # logging.info("delta_timestamp:{}".format(delta_timestamp))
    # return server_time_stamp, delta_timestamp
    return server_time_stamp

def get_compare_time(delta_timestamp) -> None:
    return get_current_timestamp() - delta_timestamp

def wait_buy_time(start_timestamp: str, advance: int=0) -> None:
    # server_timestamp, delta_timestamp = get_server_time()
    # logging.info("get_compare_time(delta_timestamp):{}".format(get_compare_time(delta_timestamp)))
    logging.info("start_timestamp:{}".format(start_timestamp))
    # while get_compare_time(delta_timestamp) < start_timestamp - advance * 1000:
    # while get_server_time() < start_timestamp - 8 * 60 * 60 *1000:
    while get_current_timestamp() < start_timestamp:
        # logging.info("Countdown of {} in {}ms".format(datetime.datetime.fromtimestamp((start_timestamp/1000)), start_timestamp-get_compare_time(delta_timestamp)))
        # logging.info("get_server_time():{}".format(get_server_time()))
        logging.info("get_current_timestamp():{}".format(get_current_timestamp()))
    return

def run(browser_type: str="Chrome", acc_pwd: dict=platform2act_pwd["tianmao_acc1"]) -> None:
    # 1. init browser driver
    web_driver: webdriver.Chrome = Driver(browser_type).driver
    # 2. open browser and login in
    logging.info("opening browser and logining in")
    login_tianmao(driver=web_driver, acc_pwd=acc_pwd)
    # 3. open maitai page
    web_driver.get(platform2url["tianmao"]["maotai_url"])
    # 4. buy on time
    date_str = datetime.datetime.now().strftime("%m.%d")
    before_text = "即将开始，{} 20:00开售".format(date_str)
    # before_text = "商品已经卖光啦，非常抱歉"
    current_timestamp = int(time.time() * 1000)
    while True:
        # if True:
        if platform2start_timestamp["tianmao"] + 60000 > current_timestamp > platform2start_timestamp["tianmao"] - 14400000:
            logging.info("Nowtime: {}, Timestamp: {}. seckill will start soon".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(time.time() * 1000)))
            try:
                wait_element = WebDriverWait(web_driver, 6).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[class*=Actions--leftButtons]"))
                )
            except Exception as e:
                logging.error("Error message while waiting before_text:{}".format(e))
            logging.info("buy_button_element_text:{}".format(wait_element.text))
            # buy_button_element_text = web_driver.find_element(by=By.CSS_SELECTOR, value="[class*=Actions--leftButtons]").text
            # for i in range(60):
            #     if buy_button_element_text == before_text:
            #         continue
            #     time.sleep(0.1)
            # logging.info("buy_button_element_text: {}".format(web_driver.find_element(by=By.CSS_SELECTOR, value="[class*=Actions--leftButtons]").text))
            WebDriverWait(web_driver, 14400).until_not(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[class*=Actions--leftButtons]"), before_text)
            )
            WebDriverWait(web_driver, 14400).until(
                EC.presence_of_element_located((By.ID, "J_LinkBuy"))
            )
            WebDriverWait(web_driver, 600, poll_frequency=0.05).until(
                EC.presence_of_element_located((By.ID, 'J_LinkBuy'))
            )
            # WebDriverWait(web_driver, 600, poll_frequency=1).until(
            #     EC.staleness_of(wait_element)
            # )
            # web_driver.refresh()
            buy_button_element = web_driver.find_element(by=By.ID, value="J_LinkBuy")
            buy_button_element_text = buy_button_element.text
            logging.info("buy_button_element_text: {}".format(buy_button_element_text))
            logging.info("Nowtime: {}, Timestamp: {}. seckill is starting".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(time.time() * 1000)))
            return
            for i in range(30):
                logging.info("buy_button_element_text: {}".format(buy_button_element_text))
                try:
                    buy_button_element.click()
                    print("buy-botton clicked!")
                    logging.info("buy-botton clicked!")
                    time.sleep(0.2)
                    # while True:
                    #     if 'detail' not in web_driver.current_url:
                    #         continue
                except Exception as e:
                    logging.error("Error message while click buy-botton:{}".format(e))
        else:
            logger.warning("Nowtime: {}, Timestamp: {}. Please check the time!!!".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(time.time() * 1000)))
    print("run over!")

def run_opt(browser_type: str, acc_pwd: dict, advance: int=0) -> None:
    # 1. init browser driver
    web_driver: webdriver.Chrome = Driver(browser_type).driver
    # 2. open browser and login in
    logging.info("opening browser and logining in")
    login_tianmao(driver=web_driver, acc_pwd=acc_pwd)
    # 3. open maitai page
    web_driver.get(platform2url["tianmao"]["maotai_cart_url"])
    # 4. buy on time
    # WebDriverWait(web_driver, 14400).until(
    #     EC.element_to_be_clickable((By.ID, "J_LinkBuy"))
    # )
    # run(browser_type="Edge", acc_pwd=acc_pwd)
    wait_buy_time(platform2start_timestamp["tianmao"], advance)
    # buy_button_element = web_driver.find_element(by=By.ID, value="J_LinkBuy")
    buy_button_element = web_driver.find_element(By.CSS_SELECTOR, value="[class=btn-area]")
    buy_button_element_text = buy_button_element.text
    logging.info("buy_button_element_text: {}".format(buy_button_element_text))
    for i in range(30):
        logging.info("buy_button_element_text: {}".format(buy_button_element_text))
        try:
            buy_button_element.click()
            print("buy-botton clicked!")
            logging.info("buy-botton clicked!")
            time.sleep(0.2)
        except Exception as e:
            logging.error("Error message while click buy-botton:{}".format(e))
    print("run_opt over!")

def test(browser_type="Edge", acc_pwd=platform2act_pwd["tianmao_acc1"]):
    # 1. init browser driver
    web_driver: webdriver.Chrome = Driver(browser_type).driver
    # 2. open browser and login in
    logging.info("opening browser and logining in")
    login_tianmao(driver=web_driver, acc_pwd=acc_pwd)
    # 3. open maitai page
    web_driver.get(platform2url["tianmao"]["maotai_buy_url"])
    buy_button_element = web_driver.find_element(by=By.ID, value="J_LinkBuy")
    buy_button_element_text = buy_button_element.text
    logging.info("buy_button_element_text: {}".format(buy_button_element_text))
    web_driver.refresh()
    buy_button_element = web_driver.find_element(by=By.ID, value="J_LinkBuy")
    buy_button_element_text = buy_button_element.text
    logging.info("buy_button_element_text: {}".format(buy_button_element_text))


if __name__ == '__main__':
    a = 1
    # run_opt(browser_type="Chrome", acc_pwd=platform2act_pwd["tianmao_acc1"])
    run(browser_type="Chrome", acc_pwd=platform2act_pwd["tianmao_acc1"])
    # t1 = threading.Thread(target=run, name="Thread-Chrome", args=("Chrome", platform2act_pwd["tianmao_acc1"]))
    # t2 = threading.Thread(target=run_opt, name="Thread-Edge", args=("Edge", platform2act_pwd["tianmao_acc2"]))
    # t1.start()
    # t2.start()
    # test()