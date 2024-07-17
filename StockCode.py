from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
import re
import time


def get_stock_code(company_name):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # 브라우저 창을 표시하지 않음
    driver = webdriver.Chrome(service=service, options=options)

    encoded_name = quote(company_name)
    search_url = f"http://data.krx.co.kr/contents/MDC/COMS/search/MDCCOMS902.cmd?keyword"
    driver.get(search_url)
    time.sleep(3)

    search_box = driver.find_element(By.XPATH, '//*[@id="jsTotSch"]')
    search_box.send_keys(company_name)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    # 결과가 로드될 때까지 대기
    stock_code_label = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="isuInfoTitle"]/label'))
    )
    stock_code = stock_code_label.text
    return stock_code

def extract_number(text):
    # 정규 표현식을 사용하여 숫자만 추출
    numbers = re.findall(r'\d+', text)
    return numbers


    #jsSearch01 > div > div.searchTb > table > tbody > tr:nth-child(1) > td:nth-child(2)