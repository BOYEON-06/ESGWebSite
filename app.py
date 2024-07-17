from flask import Flask, render_template, request, send_file, url_for
from flask_cors import CORS
import crawler
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import matplotlib
matplotlib.use('Agg')  # Agg 백엔드 사용
from urllib.parse import quote
import re
import time
import matplotlib.pyplot as plt
import io
import numpy as np

app = Flask(__name__) 
CORS(app)

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
    driver.quit()

def extract_number(text):
    # 정규 표현식을 사용하여 숫자만 추출
    numbers = re.findall(r'\d+', text)
    return numbers

def plot_stock_data(stock_code, start_date, end_date):
    print("graph를 그리는 중 입니다.")
    # 임의의 주식 데이터를 생성 (여기서는 시작 날짜와 끝 날짜를 기준으로 날짜 리스트 생성)
    dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    np.random.seed(0)
    prices = 100 + np.cumsum(np.random.randn(len(dates))) * 2  # 임의의 변동성 추가

    plt.figure(figsize=(12, 6))
    plt.plot(dates, prices, marker='o', linestyle='-', color='b', linewidth=2, markersize=5)
    plt.title(f'Stock Prices for {stock_code}', fontsize=16)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Price', fontsize=14)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 이미지 버퍼에 플롯을 저장
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()  # 플롯을 닫아서 메모리 누수 방지
    print(f'plot created for stock code {stock_code} from {start_date} to {end_date}')
    return img

    # print("graph를 그리는 중 입니다.")
    # # 임의의 주식 데이터를 생성 (여기서는 시작 날짜와 끝 날짜를 기준으로 날짜 리스트 생성)
    # dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    # prices = [100 + i for i in range(len(dates))]  # 단순히 증가하는 가격 데이터

    # plt.figure(figsize=(10, 5))
    # plt.plot(dates, prices, marker='o')
    # plt.title(f'Stock Prices for {stock_code}')
    # plt.xlabel('Date')
    # plt.ylabel('Price')
    # plt.grid(True)
    # plt.xticks(rotation=45)

    # # 이미지 버퍼에 플롯을 저장
    # img = io.BytesIO()
    # plt.savefig(img, format='png')
    # img.seek(0)
    # plt.close()
    # print(f'plot created for stock code {stock_code} from {start_date} to {end_date}')
    # return img 

@app.route('/', methods=['GET', 'POST'])
def home():
    # url = 'https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query=ESG'
    url1 = 'https://search.naver.com/search.naver?where=news&query=ESG&sm=tab_opt&sort=1&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Aall&is_sug_officeid=0&office_category=0&service_area=0'
    # url2 = ''
    img_url = None
    stock_code = None
    company_name = None

    if request.method == 'POST':
        if 'get_stock_code' in request.form:
            company_name = request.form.get('company_name')
            if company_name:
                stock_code = extract_number(get_stock_code(company_name))
                stock_code = stock_code[0]

        elif 'plot_stock_data' in request.form:
            company_name = request.form.get('company_name')
            start_date_str = request.form.get('start_date')
            end_date_str = request.form.get('end_date')
            if company_name and start_date_str and end_date_str:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                stock_code = extract_number(get_stock_code(company_name))
                stock_code = stock_code[0]
                img_url = url_for('plot_png', stock_code=stock_code, start_date=start_date_str, end_date=end_date_str)
                print(f'Generated img_url: {img_url}')

    data1 = crawler.get_data(url1)
    zipped_data = zip(data1['title'], data1['link'])
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('index.html', data=zipped_data, stock_code=stock_code, current_time=current_time, img_url=img_url, company_name=company_name)

@app.route('/plot.png')
def plot_png():
    stock_code = request.args.get('stock_code')
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    if stock_code and start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        stock_code = extract_number(get_stock_code(stock_code))
        stock_code = stock_code[0]
        img = plot_stock_data(stock_code, start_date, end_date)
        return send_file(img, mimetype='image/png')
    else:
        return "Error: Missing parameters", 400
    
if __name__ == '__main__':
    app.run(debug=True, port=3000)