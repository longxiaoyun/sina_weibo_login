#-*- coding:utf-8 -*-

# Author:longjiang

import time
import logging
from PIL import Image
import json
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.action_chains import ActionChains
from math import sqrt
import random
import os
from train_model import joblib
from process_picture import obtain_one_picture
import sys
reload(sys)
sys.setdefaultencoding("utf-8")





#微博帐号
myWeiBo = [
    ('username', 'password')
]

def image_identification(image, model_type):
    """
    :param: image
    :param: model_type
    :return:
    """
    x_data = obtain_one_picture(image)
    # deal with picture
    clr = joblib.load("model/" + model_type +".pkl")
    return clr.predict([x_data])[0]




PIXELS = []

def getType(browser):
    """ 识别图形路径 """
    ttype = ''
    time.sleep(3.5)
    im0 = Image.open(io.BytesIO(browser.get_screenshot_as_png()))
    box = browser.find_element_by_id('patternCaptchaHolder')
    im = im0.crop((int(box.location['x']) + 10, int(box.location['y']) + 100, int(box.location['x']) + box.size['width'] - 10, int(box.location['y']) + box.size['height'] - 10)).convert('L')
    im.save("save1.jpg")
    newBox = getExactly(im)
    im = im.crop(newBox)
    im.save("save2.jpg")

    px0_x = box.location['x'] + 40 + newBox[0]
    px1_y = box.location['y'] + 130 + newBox[1]
    PIXELS.append((px0_x, px1_y))
    PIXELS.append((px0_x + 100, px1_y))
    PIXELS.append((px0_x, px1_y + 100))
    PIXELS.append((px0_x + 100, px1_y + 100))


    #识别
    result = image_identification("save2.jpg", "lr")
    m_dict = joblib.load("img/m_dict.pkl")
    print("The picture class is: {}, and number path is {}".format(result, m_dict[result]))

    ttype=m_dict[result]


    return ttype



def getExactly(im):
    """ 精确剪切"""
    imin = -1
    imax = -1
    jmin = -1
    jmax = -1
    row = im.size[0]
    col = im.size[1]
    for i in range(row):
        for j in range(col):
            if im.load()[i, j] != 255:
                imax = i
                break
        if imax == -1:
            imin = i

    for j in range(col):
        for i in range(row):
            if im.load()[i, j] != 255:
                jmax = j
                break
        if jmax == -1:
            jmin = j
    return (imin + 1, jmin + 1, imax + 1, jmax + 1)

def move(browser, coordinate, coordinate0):
    """ 从坐标coordinate0，移动到坐标coordinate """
    time.sleep(0.05)
    length = sqrt((coordinate[0] - coordinate0[0]) ** 2 + (coordinate[1] - coordinate0[1]) ** 2)  # 两点直线距离
    if length < 4:  # 如果两点之间距离小于4px，直接划过去
        ActionChains(browser).move_by_offset(coordinate[0] - coordinate0[0], coordinate[1] - coordinate0[1]).perform()
        return
    else:  # 递归，不断向着终点滑动
        step = random.randint(3, 5)
        x = int(step * (coordinate[0] - coordinate0[0]) / length)  # 按比例
        y = int(step * (coordinate[1] - coordinate0[1]) / length)
        ActionChains(browser).move_by_offset(x, y).perform()
        move(browser, coordinate, (coordinate0[0] + x, coordinate0[1] + y))

def draw(browser, ttype):
    """ 滑动 """

    if len(ttype) == 4:
        px0 = PIXELS[int(ttype[0]) - 1]
        login = browser.find_element_by_id('loginAction')
        ActionChains(browser).move_to_element(login).move_by_offset(px0[0] - login.location['x'] - int(login.size['width'] / 2), px0[1] - login.location['y'] - int(login.size['height'] / 2)).perform()
        browser.execute(Command.MOUSE_DOWN, {})

        px1 = PIXELS[int(ttype[1]) - 1]
        move(browser, (px1[0], px1[1]), px0)

        px2 = PIXELS[int(ttype[2]) - 1]
        move(browser, (px2[0], px2[1]), px1)

        px3 = PIXELS[int(ttype[3]) - 1]
        move(browser, (px3[0], px3[1]), px2)
        browser.execute(Command.MOUSE_UP, {})
    else:
        print('Sorry! Failed! Maybe you need to update the code.')
        raise("draw error")


def my_default_get_cookie_from_weibo(account, password):
    driver = webdriver.Chrome('/Users/longjiang/Documents/chromedriver')
    try:
        driver.get(r'https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=')
        retry_count = 0
        while retry_count < 5 and "微博" in driver.title:
            retry_count += 1

            js = 'var lo=document.getElementById("loginWrapper");lo.style.display="block";'
            # 调用js脚本
            driver.execute_script(js)

            driver.find_element_by_id('loginName').clear()
            driver.find_element_by_id('loginName').send_keys(account)

            driver.find_element_by_id('loginPassword').clear()
            driver.find_element_by_id('loginPassword').send_keys(password)

            submit = driver.find_element_by_id('loginAction')
            ActionChains(driver).double_click(submit).perform()

            time.sleep(1)


            try:
                if driver.find_element_by_id('patternCaptchaHolder'):
                    ttype = getType(driver)  # 识别轨迹路径
                    print(ttype)
                    draw(driver, ttype)#滑动破解
            except Exception as e:
                pass

            # attempts = 0
            # success = False
            # while attempts < 6 and not success:
            #     try:
            #         if driver.find_element_by_id('patternCaptchaHolder'):
            #             ttype=getType(driver) #识别轨迹路径
            #             draw(driver, ttype)#滑动破解
            #         success = True
            #     except:
            #         attempts += 1
            #         if attempts == 3:
            #             break


            # 等待手动通过验证码(很智能，I like)
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//title[contains(text(),"我的首页")]')))


            if "我的首页" not in driver.title:
                time.sleep(4)
            if '未激活微博' in driver.page_source:
                print('账号未开通微博')
                return {}

        cookie = {}
        if "我的首页" in driver.title:
            for elem in driver.get_cookies():
                cookie[elem["name"]] = elem["value"]
            logging.warning("Get Cookie Success!( username:%s )" % account)
        return json.dumps(cookie)
    except Exception as e:
        logging.warning("登录失败 %s!" % account)
        logging.error(e)
        return ""
    finally:
        try:
            driver.quit()
        except Exception as e:
            logging.error(e)
            pass

#获取cookies
def getCookie(account, password):
    return my_default_get_cookie_from_weibo(account, password)



def initCookie(rconn, spiderName):
    """ 获取所有账号的Cookies，存入Redis。如果Redis已有该账号的Cookie，则不再获取。 """
    for weibo in myWeiBo:
        if rconn.get("%s:Cookies:%s--%s" % (spiderName, weibo[0], weibo[1])) is None:  # 'SinaSpider:Cookies:账号--密码'，为None即不存在。
            cookie = getCookie(weibo[0], weibo[1])
            if len(cookie) > 0:
                rconn.set("%s:Cookies:%s--%s" % (spiderName, weibo[0], weibo[1]), cookie)

                print("%s:Cookies:%s--%s" % (spiderName, weibo[0], weibo[1]), cookie)
    print('%s' %key for key in rconn.keys())
    cookieNum = "".join('%s' %key for key in rconn.keys()).count("SinaSpider:Cookies")
    logging.warning("The num of the cookies is %s" % cookieNum)
    if cookieNum == 0:
        logging.warning('Stopping...')
        os.system("pause")


def updateCookie(accountText, rconn, spiderName):
    """ 更新一个账号的Cookie """
    account = accountText.split("--")[0]
    password = accountText.split("--")[1]
    cookie = getCookie(account, password)
    if len(cookie) > 0:
        logging.warning("The cookie of %s has been updated successfully!" % account)
        rconn.set("%s:Cookies:%s" % (spiderName, accountText), cookie)
    else:
        logging.warning("The cookie of %s updated failed! Remove it!" % accountText)
        removeCookie(accountText, rconn, spiderName)


def removeCookie(accountText, rconn, spiderName):
    """ 删除某个账号的Cookie """
    rconn.delete("%s:Cookies:%s" % (spiderName, accountText))
    cookieNum = "".join(rconn.keys()).count("SinaSpider:Cookies")
    logging.warning("The num of the cookies left is %s" % cookieNum)
    if cookieNum == 0:
        logging.warning("Stopping...")
        os.system("pause")



if __name__ == '__main__':
    my_default_get_cookie_from_weibo('15211452000', 'rkalpq227')