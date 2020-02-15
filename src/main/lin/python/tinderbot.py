# IMPORTS
import os
from selenium import webdriver
from time import sleep

# LOCAL MODULE IMPORTS
# APPEND PATH
if 'PYDEVD_LOAD_VALUES_ASYNC' in os.environ:
    import sys
    sys.path.append(os.getcwd()+'\\src\\main\\lin\\python')

from mypath import get_path, my_cd
from credentials import username, password


class TinderBot:
    def __init__(self):
        self.root_path = get_path('root_path')
        self.data_path = get_path('data_path')
        self.data_path = get_path('dir_path')
        self.data_path = get_path('file_path')
        self.driver = webdriver.Chrome(self.root_path + '/bin/chromedriver.exe')

    def login(self):
        self.driver.get('https://tinder.com')

        sleep(2)

        fb_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/div[2]/button')
        fb_btn.click()

        # switch to login popup
        base_window = self.driver.window_handles[0]
        self.driver.switch_to.window(self.driver.window_handles[1])

        email_in = self.driver.find_element_by_xpath('//*[@id="email"]')
        email_in.send_keys(username)

        pw_in = self.driver.find_element_by_xpath('//*[@id="pass"]')
        pw_in.send_keys(password)

        login_btn = self.driver.find_element_by_xpath('//*[@id="u_0_0"]')
        login_btn.click()

        self.driver.switch_to.window(base_window)

        popup_1 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]/span')
        popup_1.click()

        popup_2 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]/span')
        popup_2.click()

    def like(self):
        like_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[3]/span/svg')
        like_btn.click()

    def dislike(self):
        dislike_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[1]/span/svg')
        dislike_btn.click()

    def auto_swipe(self):
        while True:
            sleep(0.5)
            try:
                self.like()
            except Exception:
                try:
                    self.close_popup()
                except Exception:
                    self.close_match()

    def close_popup(self):
        popup_3 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]')
        popup_3.click()

    def close_match(self):
        match_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
        match_popup.click()

    def save_image(self):
        image = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[1]/span/a[2]/div/div[1]/div/div[2]/div/div')
        with open(self.data_path + '\\tinder\\image.png', 'wb') as file:
            file.write(image.screenshot_as_png)

if __name__ == "__main__":

    bot = TinderBot()
    bot.login()
