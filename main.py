from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
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
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'iconfont icon-password')))
    driver.find_element(by=By.ID, value='fm-login-id').send_keys(platform2act_pwd["tianmao"]["account"])
    driver.find_element(by=By.ID, value='fm-login-password').send_keys(platform2act_pwd["tianmao"]["password"])
    driver.find_element(by=By.CLASS_NAME, value='fm-btn').click()
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

def buy_on_time(driver, buytime):

    driver.get('https://www.maotai.com/')
    driver.find_element_by_link_text('茅台商城').click()
    time.sleep(3)

    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        if now > buytime:
            driver.find_element_by_id('btn-reservation').click()
            driver.find_element_by_link_text('立即抢购').click()
            time.sleep(0.5)
            driver.find_element_by_link_text('去购物车结算').click()
            driver.find_element_by_link_text('去结算').click()
            driver.find_element_by_link_text('提交订单').click()
            print('抢购成功！')
            break
        time.sleep(0.1)

if __name__ == '__main__':
    # 1. init browser driver
    chrome_driver = ChromeDriver().driver
    # 2. open browser and login in
    print("opening browser and logining in")
    login(driver=chrome_driver, platform="tianmao")
    
    # 3. open maitai page
    chrome_driver.get(platform2url["tianmao"]["maotai_url"])
    
    # 4. buy on time
    # time.sleep(6)
    # buy_button_element_text = ""
    # while not buy_button_element_text:
    #     buy_button_element = chrome_driver.find_element(by=By.CSS_SELECTOR, value="[class*=Actions--leftButtons]")
    #     buy_button_element_text = buy_button_element.text
    # buy_button_element = chrome_driver.find_element(by=By.CSS_SELECTOR, value="[class*=Actions--leftButtons]")
    # buy_button_element_text = buy_button_element.text
    # print("buy_button_element_text:", type(buy_button_element_text), buy_button_element_text)
    # WebDriverWait(chrome_driver, 10).until(
    #     EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[class*=Actions--leftButtons]"), "商品已经卖光啦，非常抱歉")
    # )
    buy_button_element = chrome_driver.find_element(by=By.CSS_SELECTOR, value="[class*=Actions--leftButtons]")
    buy_button_element_text = buy_button_element.text
    while True:
        print("buy_button_element_text:", type(buy_button_element_text), buy_button_element_text)
        current_timestamp = int(time.time() * 1000)
        if current_timestamp > platform2start_timestamp["tianmao"] - 180000:
        # if True:
            logger.info("Nowtime: {}, Timestamp:{}. seckill will start in about 3 min".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(time.time() * 1000)))
            # buy_button_element.refresh()
            WebDriverWait(chrome_driver, 240).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[class*=Actions--leftButtons]"), "立即购买")
            )
            buy_button_element = chrome_driver.find_element(by=By.CSS_SELECTOR, value="[class*=Actions--leftButtons]")
            buy_button_element_text = buy_button_element.text
            print("buy_button_element_text:", type(buy_button_element_text), buy_button_element_text)
            logger.info("Nowtime: {}, Timestamp:{}. seckill is starting".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(time.time() * 1000)))
            try:
                for i in range(10):
                    buy_button_element.click()
                    print("botton clicked")
                    time.sleep(0.1)
                while True:
                    if 'detail' not in chrome_driver.current_url:
                        continue
            except NoSuchElementException:
                print("click botton failed")
        else:
            time.sleep(60)
    print("closing browser")

