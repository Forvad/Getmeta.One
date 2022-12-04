from time import sleep
from requests import get
from json import loads
from threading import Thread
from random import choice

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import Select


class GetMeta:
    def __init__(self, reff):
        self.driver = self.create_driver()
        self.reff = reff

    @staticmethod
    def create_driver():
        opt = webdriver.ChromeOptions()
        opt.add_extension('Free-VPN-for-ChromeVPN-Proxy-VeePN.crx')
        opt.add_argument(f"--user-agent={UserAgent().chrome}")
        # opt.add_argument("--headless")
        # opt.add_argument('--no-sandbox')
        # opt.add_argument("--disable-gpu")
        opt.add_experimental_option('prefs', {'intl.accept_languages': 'ru,en,ru-BY,ru-RU,en-US'})
        driver = webdriver.Chrome(chrome_options=opt)
        return driver

    @staticmethod
    def runs(driver, button):
        driver.execute_script("arguments[0].click();", button)

    def vpn(self):
        driver = self.driver
        sleep(5)
        driver.switch_to.window(driver.window_handles[0])
        driver.get('chrome-extension://majdfhpaihoncoakbjgbdhglocklcgno/html/foreground.html')
        sleep(2)
        self.runs(driver,
                  driver.find_element('xpath', '//*[@id="screen-tooltips-template"]/div[2]/div/div[3]/div/div/button'))
        sleep(4)
        self.runs(driver,
                  driver.find_element('xpath', '//*[@id="screen-tooltips-template"]/div[2]/div/div[3]/div/div/button'))
        sleep(1)
        self.runs(driver, driver.find_element('xpath', '// *[ @ id = "mainBtn"] / span'))
        sleep(3)

    def mail2(self):
        name = self.get_username()
        self.vpn()
        sleep(3)
        driver = self.driver
        driver.implicitly_wait(15)
        driver.get(self.reff)
        sleep(5)
        driver.find_element('xpath', "//img[@alt='Main landing MetaOne Power button']").click()
        sleep(2)
        read_mores = driver.find_elements('xpath', '//*[@id="join"]/div[2]/div[1]/div[1]/div/input')
        for read_more in read_mores:
            driver.execute_script("arguments[0].scrollIntoView();", read_more)
        sleep(2)
        driver.find_element('xpath', '//*[@id="join"]/div[2]/div[1]/div[1]/div/input').send_keys(f'{name}@1secmail.com')
        sleep(2)
        driver.find_element('xpath', '//*[@id="join"]/div[2]/div[1]/div[2]/div/input').send_keys(name)
        sleep(2)
        driver.find_element('xpath', '//*[@id="join"]/div[2]/div[1]/div[4]/button/div').click()
        sleep(4)
        password = self.verf_mail(name)
        inputs = driver.find_element(By.XPATH, '//*[@id="join"]/div[2]/div[2]/div[2]/div[4]/input')
        inputs.click()
        inputs.send_keys(password[0])
        for i in range(2, 7):
            inputs = driver.find_element(By.XPATH, f'//*[@id="join"]/div[2]/div[2]/div[2]/div[4]/input[{i}]')
            inputs.click()
            inputs.send_keys(password[i - 1])
            sleep(0.5)
        sleep(2)
        driver.find_element('xpath', "//section[@id='join']/div[2]/div[2]/div[2]/div[8]/div[2]").click()
        sleep(2)
        driver.find_element('xpath', "//section[@id='join']/div[2]/div[2]/div[2]/div[4]/div/div[2]/div/select").click()
        sleep(2)
        Select(driver.find_element('xpath',
            "//section[@id='join']/div[2]/div[2]/div[2]/div[4]/div/div[2]/div/select")).select_by_visible_text("Belarus")
        sleep(2)
        driver.find_element('xpath', '//*[@id="join"]/div[2]/div[2]/div[2]/div[4]/div/div[2]/input')\
            .send_keys(f"29{self.get_number()}")
        sleep(2)
        driver.find_element('xpath', "//section[@id='join']/div[2]/div[2]/div[2]/div[7]/div[2]").click()
        sleep(5)
        driver.quit()

    @staticmethod
    def verf_mail(login):
        for _ in range(10):
            r = get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain=1secmail.com')
            if len(loads(r.text)) >= 1:
                text = loads(r.text)[0]["id"]
                g = get(
                    f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain=1secmail.com&id={text}')
                texts = loads(g.text)['body']
                soup = BeautifulSoup(texts, 'html.parser')
                soup = soup.findAll(class_='col-lge')
                return str(soup).split('600;">')[2].split('</p>')[0]
            else:
                sleep(2)

    @staticmethod
    def get_username():
        return "".join([choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ013456789") for _ in range(8)]).lower()

    @staticmethod
    def get_number():
        return ''.join([choice('0123456789') for _ in range(7)])


def run(refs):
    try:
        main = GetMeta(refs)
        main.mail2()
    except:
        sleep(5)


if __name__ == '__main__':
    ref = input('Ваша реф ссылка: ')
    num = int(input('Выберите колличество заходов: '))
    num_Thread = int(input('Сколько процессов(окон браузера за раз): '))
    a = 0
    while a < num:
        theand = []
        for i in range(a, a + num_Thread):
            go = Thread(target=run, args=(ref, ))
            theand.append(go)
            go.start()

        [thread.join() for thread in theand]
        a += num_Thread
        print(f'Кошелёк № {a}')

