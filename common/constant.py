import time
import datetime

def get_the_timestamp(delta_time_stamp=0):
    now_day_struct_time = datetime.datetime.now().date().timetuple()
    now_day_timestamp = int(time.mktime(now_day_struct_time) * 1000)
    the_timestamp = now_day_timestamp + delta_time_stamp * 1000
    return the_timestamp

platform2act_pwd = {
    "tianmao_acc1": {
        "account" : "18827201249",
        "password" : "FJL960929"
    },
    "tianmao_acc2": {
        "account" : "18827201249",
        "password" : "FJL960929"
    }
}

platform2url = {
    "tianmao": {
        "login_url": "https://login.tmall.com/",
        "maotai_url": "https://chaoshi.detail.tmall.com/item.htm?addressId=17891842192&id=20739895092"
    },
    "jingdong": {
        "login_url": "https://passport.jd.com/new/login.aspx",
        "maotai_url": ""
    }
}

platform2start_timestamp = {
    "tianmao": get_the_timestamp(72000),
    "jingdong": ""
}
