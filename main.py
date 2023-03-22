from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
import time
from common.constant import jingdong, tianmao  

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

def frame_is_exist(url):
    # 创建一个浏览器实例
    driver = webdriver.Chrome()
    # 打开页面
    driver.get(url)
    # 获取页面中所有的frame元素
    frames = driver.find_element(by=By.TAG_NAME, value="frame") + driver.find_element(by=By.TAG_NAME, value="iframe")
    # 如果frames列表不为空，则页面中存在frame
    if frames:
        print("页面中存在frame")
    else:
        print("页面中不存在frame")
    # 关闭浏览器
    driver.quit()


def login_jingdong(driver):
    driver.get(jingdong["login_url"])
    driver.find_element(by=By.LINK_TEXT, value='账户登录').click()
    driver.find_element(by=By.NAME, value='loginname').send_keys('18827201249')
    driver.find_element(by=By.NAME, value='nloginpwd').send_keys('FJL960929')
    driver.find_element(by=By.ID, value='loginsubmit').click()
    while 'login' in driver.current_url:
        print(driver.current_url)
        time.sleep(1)

def login_tianmao(driver):
    driver.get(tianmao["login_url"])
    time.sleep(5)
    driver.switch_to.frame(driver.find_element(by=By.ID, value='J_loginIframe'))
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'iconfont icon-password')))
    driver.find_element(by=By.ID, value='fm-login-id').send_keys('18827201249')
    driver.find_element(by=By.ID, value='fm-login-password').send_keys('FJL960929')
    driver.find_element(by=By.CLASS_NAME, value='fm-btn').click()
    while 'login' in driver.current_url:
        print(driver.current_url)
        time.sleep(1)

def login(driver, platform):
    match platform:
        case "jingdong":
            login_jingdong(driver)
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
    tianmao_maitai_url = "https://chaoshi.detail.tmall.com/item.htm?addressId=17891842192&id=20739895092"
    frame_is_exist(tianmao_maitai_url)
    chrome_driver.get(tianmao_maitai_url)
    
    # 4. buy on time
    element = chrome_driver.find_element(by=By.ID, value="root").find_element
    
    
    element = chrome_driver.find_element(by=By.XPATH, value="/html/body/div[4]/div/div[2]/div[1]/div[1]/div/div[2]/div[7]/div[1]/button/span")
    print(element)
    # buytime = '2022-01-01 00:00:00.000000'
    # buy_on_time(buytime)

    print("closing browser")

