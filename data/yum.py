from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from datetime import datetime
import pandas as pd
import os

now = datetime.now().isoformat()

if not os.path.exists("data"):
   os.makedirs("data")

if not os.path.exists("data/" + now):
   os.makedirs("data/" + now)

url = "https://www.sis.itu.edu.tr/EN/student/course-schedules/course-schedules.php?seviye=LS&derskodu="
options = FirefoxOptions()
options.add_argument("--start-minimized")
options.add_argument("--log-level=0")
options.add_argument("--headless")

browser = Firefox(executable_path="geckodriver", options=options, service_log_path="/dev/null")
browser.get(url)

dropdown_button = browser.find_element(by=By.CSS_SELECTOR, value=".bs-placeholder")
dropdown_button.click()
course_code_elements = browser.find_elements(by=By.XPATH, value="/html/body/div/div[2]/div/div[1]/form/div[2]/div/div[2]/ul/*")
course_codes = []

for i in range(len(course_code_elements)):
    if (i == 0) : continue
    course_codes.append(browser.find_element(by=By.CSS_SELECTOR, value=f'#bs-select-2-{i} > span:nth-child(1)').text)

for course in course_codes:
    browser.get(url=url+course)

    table = browser.find_element(by=By.CSS_SELECTOR, value=".table")
    rows = table.find_elements(by=By.CSS_SELECTOR, value="tr")
    columns = rows[1].find_elements(by=By.CSS_SELECTOR, value="td")
    col_data = [col.text for col in columns]

    rows = rows[2:]
    row_data = []
    if len(rows) != 0:
        for row in rows:
            cols = row.find_elements(by=By.CSS_SELECTOR, value="td")
            cols = [col.text for col in cols]
            row_data.append(cols)
    
    df = pd.DataFrame(data=row_data, columns=col_data)
    df.to_csv(path_or_buf="data/" + now + "/" + course + ".csv")
