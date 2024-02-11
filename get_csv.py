from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import requests
from bs4 import BeautifulSoup

DEFAULT_DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "data")
USER_DATA_DIR = "C:\\Users\\lukas\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1"
class SportsCSV():
    def __init__(self):
        pass
    
    def check_allow_button(self):
        allow_button = self.driver.find_elements(By.CSS_SELECTOR, "#legacyContent > div > div > form > input.patreon-button.patreon-button-action")
        if len(allow_button) > 0:
            allow_button[0].click()
            return True
        return False

    def __extractCookiesFromDriver(self):
        headers = {}
        self.s = requests.session()
        self.s.headers.update(headers)
        for cookie in self.driver.get_cookies():
            c = {cookie["name"]: cookie["value"]}
            self.s.cookies.update(c)

    def login(self):
        patronButton = self.driver.find_elements(By.XPATH, "/html/body/div/div/a")
        if len(patronButton) > 0:
            patronButton[0].click()
            
            if self.check_allow_button():
                return True
            
            self.driver.save_screenshot("screenshot.png")
            
            email_input = self.wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "input[type=email]")))
            email_input.send_keys(os.environ["EMAIL"])

            continue_button = self.driver.find_element(By.CSS_SELECTOR, "#renderPageContentWrapper > div.sc-xo4ne6-0.fmNaoE > div > div > form > div:nth-child(3) > button")
            continue_button.click()

            time.sleep(1)

            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[type=password]")
            password_input.send_keys(os.environ["PASSWORD"])

            continue_button.click()

            time.sleep(1)

            self.check_allow_button()

            self.__extractCookiesFromDriver()

            return True
        self.__extractCookiesFromDriver()
        return False

    def goTo(self, url):
        self.driver.get(url)

        if self.login():
            # retry after the login function has logged in
            self.driver.get(url)

    def setupMethod(self):
        options = uc.ChromeOptions()
        # default directory to data folder in current working directory (cwd)
        prefs = {"download.default_directory": DEFAULT_DOWNLOAD_FOLDER}
        options.add_experimental_option("prefs", prefs)
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--verbose')
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--start-maximized')
        options.add_argument('--user-data-dir=' + USER_DATA_DIR)
        self.driver = uc.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        self.wait = WebDriverWait(self.driver, 180)

    def getDatapoint(self, datapoint):
        self.__fullLogin()

        r = self.s.get(f"https://tracking.pbpstats.com/stats-nba-tracking-game-logs?Season=2023-24&SeasonType=RegularSeason&Type=player&StatMeasure={datapoint}&TeamId=&OpponentTeamId=")
        soup = BeautifulSoup(r.content, "html.parser")
        rows = []
        for row in soup.find_all("tr"):
             data = map(lambda x: x.text, row.findChildren(["td", "th"], recursive=False))
             rows.append(list(data))

        return rows

    def __fullLogin(self):
        self.setupMethod()
        self.goTo("https://tracking.pbpstats.com/stats-nba-tracking-export")
        self.teardownMethod()

    def trackingExport(self, path):
        self.__fullLogin()

        season = "2023-24"
        seasonType = "RegularSeason"
        tracking_type = "game_logs"
        
        r = self.s.get(f"https://tracking.pbpstats.com/get-tracking-csv?Season={season}&SeasonType={seasonType}&Type={tracking_type}")
        open(path, "wb").write(r.content)


    def teardownMethod(self):
        self.driver.quit()

