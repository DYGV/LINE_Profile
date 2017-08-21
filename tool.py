# coding :utf-8
import time
import urllib.request
import io
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def line_profile(address, password):
    phantomjs_path = 'path to phantomjs.exe'
    try:
        f = open(phantomjs_path)
    except FileNotFoundError as e:
        raise
    driver = webdriver.PhantomJS(phantomjs_path,
                                 desired_capabilities={'phantomjs.page.settings.resourceTimeout': '10000'})

    wait = WebDriverWait(driver, 30)

    driver.get("https://timeline.line.me/")  # access to this address
    driver.find_element_by_class_name('i1').click()  # Click login button
    time.sleep(5)

    wait.until(lambda driver: driver.current_url != "https://timeline.line.me/")  # to wait the change from first page
    print(driver.current_url)

    elem_id = driver.find_element_by_id('id')  # e-mail address input place
    elem_id.send_keys(address)
    elem_password = driver.find_element_by_id('passwd')  # e-mail address input place
    elem_password.send_keys(password)

    driver.find_element_by_class_name('MdBtn03Login').click()  # Click the Login button

    wait.until(lambda driver: driver.current_url == "https://timeline.line.me/")
    wait.until(EC.presence_of_all_elements_located)
    driver.implicitly_wait(10)

    driver.find_element_by_xpath('//*[@class="sp sp_gnb_friends _c_ex"]').click()  # Click the friends list button
    wait.until(EC.presence_of_all_elements_located)
    driver.implicitly_wait(10)

    n = driver.find_element_by_tag_name("em").text  # find the friends number to calculate scroll count

    wait.until(EC.presence_of_all_elements_located)
    time.sleep(3)

    for scroll_count in range(0, int(n) // 19):  # calculate scroll count
        # scroll list using javascript
        driver.execute_script('document.getElementsByClassName("friends_list")[0].scrollIntoView(false);')
    time.sleep(5)

    data = BeautifulSoup(driver.page_source.encode('utf-8'))
    time.sleep(5)

#    for friends_list in data.find_all('ul', attrs={'class': 'friends_list'}):
    for friends_list_li in data.select("ul.friends_list > li"):
        name = friends_list_li.find("dt", class_="friend_name")
        img = friends_list_li.find("img", class_="")
        print(name.span.string)
        print(img["src"])

        try:
            req_img = urllib.request.urlopen(img["src"])
            image_file = io.BytesIO(req_img.read())
            im = Image.open(image_file)
            im.save("./profile_img/{0}.jpg".format(name.span.string))
        except:
            pass

if __name__ == "__main__":

    address = input('enter a e-mail address: ')
    password = input('enter a password: ')
    print("Please wait...")
    line_profile(address, password)
