from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.nba.com/stats/players/traditional")

wait = WebDriverWait(driver, 180)

select_pages = Select(wait.until(expected_conditions.presence_of_element_located((By.XPATH, """//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[3]/div/label/div/select"""))))
select_pages.select_by_value("-1")

links = driver.find_elements(By.CSS_SELECTOR, "tr > td:nth-child(2) > a")

df = pandas.DataFrame(columns=["id", "name"])

for i, link in enumerate(links):
    df.loc[i] = [link.get_attribute("href").split("/")[5], link.text]

df.to_csv("NBA_Player_IDs.csv", index=False)

driver.quit()