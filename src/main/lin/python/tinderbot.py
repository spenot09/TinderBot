########################################################################################################################
# IMPORTS
########################################################################################################################
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import time, sleep

# PATH
if 'PYDEVD_LOAD_VALUES_ASYNC' in os.environ:
    import sys
    sys.path.append(os.getcwd()+'\\src\\main\\lin\\python')

# LOCAL MODULE IMPORTS
from mypath import get_path
from credentials import username, password


########################################################################################################################
# TINDERBOT
########################################################################################################################
class TinderBot:
    def __init__(self):
        self.root_path = get_path('root_path')
        self.data_path = get_path('data_path')
        self.dir_path = get_path('dir_path')
        self.file_path = get_path('file_path')
        self.driver = webdriver.Chrome(os.path.join(self.root_path, 'bin', 'chromedriver.exe'))
        self.image = None

    def login(self):
        self.driver.maximize_window()
        self.driver.get('https://tinder.com')

        sleep(3)

        fb_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button')
        if fb_btn.text == 'LOGIN WITH FACEBOOK':
            fb_btn.click()
        else:
            if fb_btn.text == 'LOG IN WITH PHONE NUMBER':
                more_opt_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/button')
                more_opt_btn.click()
            fb_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[3]/button')
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

        sleep(5)

        try:
            popup_1 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
        except:
            popup_1 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]/span')
        popup_1.click()

        try:
            popup_2 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]')
        except:
            popup_2 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]/span')
        popup_2.click()

    def check_exists_by_xpath(self, xpath):
        """Check if an xpath exists"""
        try:
            self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def like(self):
        try:
            self.driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_RIGHT)
        except:
            like_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[2]/div/button[3]')
            like_btn.click()

    def super_like(self):
        try:
            self.driver.find_element_by_tag_name('body').send_keys(Keys.ENTER)
        except:
            like_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[2]/div/button[2]')
            like_btn.click()

    def dislike(self):
        try:
            self.driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_LEFT)
        except:
            dislike_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[2]/div/button[1]')
            dislike_btn.click()

    def press_space(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.SPACE)

    def press_up(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_UP)

    def press_down(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_DOWN)

    def close_popup(self):
        popup_3 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]')
        popup_3.click()

    def close_match(self):
        match_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')
        match_popup.click()

    def scrape_images(self, save_dir):
        self.press_up()
        xpath_base = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[1]/span/a[2]/div/div[1]/div'
        image_num = 1
        xpath = xpath_base + f'/div[{image_num}]/div/div'
        while True:
            try:
                self.image = self.driver.find_element_by_xpath(xpath)
            except:
                break
            else:
                self.save_image(os.path.join(save_dir, f'{time()}_{image_num}.png'))
                self.press_space()
                image_num += 1
                xpath = xpath_base + f'/div[{image_num}]/div/div'

    def save_image(self, save_path):
        with open(save_path, 'wb') as file:
            file.write(self.image.screenshot_as_png)

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

    def manual_classify(self):
        while True:
            classify = input()
            try:
                if classify == 'superlike' or classify == 's':
                    save_dir = os.path.join(self.data_path, 'tinder', 'superlike')
                    self.scrape_images(save_dir)
                    self.super_like()
                elif classify == 'like' or classify == 'l':
                    save_dir = os.path.join(self.data_path, 'tinder', 'like')
                    self.scrape_images(save_dir)
                    self.like()
                elif classify == 'dislike' or classify == 'd':
                    save_dir = os.path.join(self.data_path, 'tinder', 'dislike')
                    self.scrape_images(save_dir)
                    self.dislike()
                else:
                    print("You must enter 'superlike', 'like' or 'dislike'")
                    continue
            except Exception as e:
                print("Error:", e)
                break

    def check_new_matches(self):
        xpath = '//*[@id="match-tab"]/span'
        if self.check_exists_by_xpath(xpath):
            matches = int(self.driver.find_element_by_xpath(xpath).text)
        else:
            matches = 0
        return matches

    def send_message_matches(self, match_number, message, send=False):
        if match_number % 9 == 0:
            row = match_number // 9
            col = 9
        else:
            row = match_number // 9 + 1
            col = match_number % 9
        row = int(match_number/9)+1
        xpath = f'//*[@id="matchListNoMessages"]/div[{row}]/div[{col}]/a/div[1]'
        self.driver.find_element_by_xpath(xpath).click()
        message_box = '//*[@id="chat-text-area"]'
        self.driver.find_element_by_xpath(message_box).send_keys(message)
        if send:
            send_button = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/form/button'
            self.driver.find_element_by_xpath(send_button).click()
        return

    def send_messages_all_new_matches(self, send=False):
        while self.check_new_matches() != 0:
            message = input()
            self.send_message_matches(self.check_new_matches()+1, message, send)


def path_dump():
    """
    Dump of useful paths
    """
    # Match popup
    name = '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/div[2]'
    keep_swiping = '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a'
    say_something = '//*[@id="chat-text-area"]'
    send_message = '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/div[3]/form/button'

    # Matches list
    first_match = '//*[@id="matchListNoMessages"]/div[1]/div[2]/a/div[1]'
    red_button = '//*[@id="matchListNoMessages"]/div[1]/div[2]/a/div[3]'
    message_box = '//*[@id="chat-text-area"]'
    send_message = '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div/div/div[3]/form/button'
    name = '//*[@id="SC.chat_5e480856be30ea0100107aec5e496690bce67e0100b9807c"]/div/div/h3/span'


if __name__ == "__main__":

    bot = TinderBot()
    bot.login()
    # bot.manual_classify()
