from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import requests

DEFAULT_DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "data")

class SportsCSV():
    def __init__(self):
        #self.userDataDir = userDataDir
        pass

    def login(self):
        patronButton = self.driver.find_elements(By.XPATH, "/html/body/div/div/a")
        if len(patronButton) > 0:
            patronButton[0].click()
            email_input = self.wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "input[type=email]")))
            email_input.send_keys(os.environ["EMAIL"])

            continue_button = self.driver.find_element(By.CSS_SELECTOR, "#renderPageContentWrapper > div.sc-xo4ne6-0.fmNaoE > div > div > form > div:nth-child(3) > button")
            continue_button.click()

            time.sleep(1)

            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[type=password]")
            password_input.send_keys(os.environ["PASSWORD"])

            continue_button.click()

            time.sleep(1)

            allow_button = self.driver.find_element(By.CSS_SELECTOR, "#legacyContent > div > div > form > input.patreon-button.patreon-button-action")
            allow_button.click()

            self.driver.save_screenshot("screenshot.png")

            return True
        return False

    def goTo(self, url):
        self.driver.get(url)

        if self.login():
            # retry after the login function has logged in
            self.driver.get(url)

    def setupMethod(self):
        options = uc.ChromeOptions()
        # default directory to data folder in current working directory (cwd)
        #options.add_argument("user-data-dir=" + self.userDataDir)
        prefs = {"download.default_directory": DEFAULT_DOWNLOAD_FOLDER}
        options.add_experimental_option("prefs", prefs)
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        #options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        self.driver = uc.Chrome(driver_executable_path="/home/backyardsubsistence/.local/share/undetected_chromedriver/chromedriver", options=options)
        self.wait = WebDriverWait(self.driver, 180)

    # def getDatapoint(self, datapoint):
    #     self.goTo(f"https://tracking.pbpstats.com/stats-nba-tracking-game-logs?Season=2023-24&SeasonType=RegularSeason&Type=player&StatMeasure={datapoint}&TeamId=&OpponentTeamId=")

    #     export_csv_button = self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div/div/div[1]/button")))
    #     export_csv_button.click()

    #     time.sleep(10) # wait for download

    #     downloaded_file_path = os.path.join(DEFAULT_DOWNLOAD_FOLDER, "csv.csv")
    #     if os.path.exists(downloaded_file_path):
    #         os.rename(downloaded_file_path, os.path.join(DEFAULT_DOWNLOAD_FOLDER, datapoint + ".csv"))

    # def getAllDatapoints(self):
    #     datapoints = ["Defense", "Drives", "ElbowTouch", "PaintTouch", "Passing", "Possesions", "Rebounding", "SpeedDistance", "PostTouch"]
    #     for datapoint in datapoints:
    #         self.setupMethod()
    #         self.getDatapoint(datapoint)
    #         self.teardownMethod()
        
    def trackingExport(self, path):
        self.setupMethod()
        # login
        self.goTo("https://tracking.pbpstats.com/stats-nba-tracking-export")

        season = "2023-24"
        seasonType = "RegularSeason"
        tracking_type = "game_logs"
        headers = {}
        s = requests.session()
        s.headers.update(headers)
        for cookie in self.driver.get_cookies():
            c = {cookie["name"]: cookie["value"]}
            s.cookies.update(c)
        r = s.get(f"https://tracking.pbpstats.com/get-tracking-csvSeason={season}&SeasonType={seasonType}&Type={tracking_type}")
        self.teardownMethod()
        open(path, "wb").write(r.content)


    def teardownMethod(self):
        self.driver.quit()
