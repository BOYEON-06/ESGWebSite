import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Define start and end dates
start = datetime.datetime(2023, 7, 15)
end = datetime.datetime(2024, 7, 15)

# Fetch historical stock data for Samsung Electronics (005930.KS) from Yahoo Finance using yfinance
samsung = yf.download("005930", start=start, end=end)

print("<Samsung Electronics Co. Ltd (005930.KS) 주가 Historical Data>\n")
print(samsung)
print('\n')
print(samsung.info())

# # 거래량이 0인 일자 제거 & 수정종가 데이터만 사용
# data = samsung['Adj Close'][samsung['Volume'] != 0] 

# def plot_rolling(data, interval):
#     rolmean = data.rolling(interval).mean()
#     rolstd = data.rolling(interval).std()
#     #Plot rolling statistics:
#     plt.figure(figsize=(10, 6))
#     plt.xlabel('Date')
#     orig = plt.plot(data, color='blue',label='Original')
#     mean = plt.plot(rolmean, color='red', label='Rolling Mean {}'.format(interval))
#     std = plt.plot(rolstd, color='black', label = 'Rolling Std {}'.format(interval))
#     plt.legend(loc='best')
#     plt.title('Rolling Mean & Standard Deviation')
#     plt.show()

# # 50일치 평균내어 이동평균계산
# plot_rolling(data, 50)

# # 원본데이터 ADF 테스트
# from statsmodels.tsa.stattools import adfuller

# def adf_test(data):
#     result = adfuller(data.values)
#     print('ADF Statistics: %f' % result[0])
#     print('p-value: %f' % result[1])
#     print('num of lags: %f' % result[2])
#     print('num of observations: %f' % result[3])
#     print('Critical values:')
#     for k, v in result[4].items():
#         print('\t%s: %.3f' % (k,v))

# # 1차 차분 데이터 diff1
# dff1 = data.diff().dropna()
# dff1.plot(figsize=(15,5))

# # # ACF, PACF plot 
# # from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
# # plot_acf(data)
# # plot_pacf(data)
# # plt.show()

# import pmdarima as pm
# from pmdarima.arima import ndiffs
# data = samsung['Adj Close']
# n_diffs = ndiffs(data, alpha=0.05, test='adf', max_d=6)
# # print(f"추정된 차수 d = {n_diffs}") 

# model = pm.auto_arima(
#             y=data, 
#             d=1, 
#             start_p=0, max_p=3, 
#             start_q=0, max_q=3, 
#             m=1, seasonal=False, # 계절성이 없음!
#             stepwise=True,
#             trace=True
# )
# # model.plot_diagnostics(figsize=(16,8))
# # plt.show()
# # print(model.summary())

# # train : test = 9 : 1
# train_data, test_data = data[:int(len(data)*0.9)], data[int(len(data)*0.9):]

# # train_data 모델 학습
# from statsmodels.tsa.arima_model import ARIMA

# model_fit = pm.auto_arima(
#     	    y=train_data, 
#  	        d=n_diffs , 
#             start_p=0, max_p=2, 
#             start_q=0, max_q=2, 
#             m=1, seasonal=False, # 계절성이 없음!
#             stepwise=True,
#             trace=True
# )
# # print(model_fit.summary())

# # forecast 함수
# def forecast_n_step(model, n = 1):
#     fc, conf_int = model.predict(n_periods=n, return_conf_int=True)
#     # print("fc", fc,"conf_int", conf_int)
#     return (
#         fc.tolist()[0:n], np.asarray(conf_int).tolist()[0:n]
#    )

# def forecast(len, model, index, data=None):
#     y_pred = []
#     pred_upper = []
#     pred_lower = []

#     if data is not None:
#         for new_ob in data:
#             fc, conf = forecast_n_step(model)
#             y_pred.append(fc[0])
#             pred_upper.append(conf[0][1])
#             pred_lower.append(conf[0][0])
#             model.update(new_ob)
#     else:
#         for i in range(len):
#             fc, conf = forecast_n_step(model)
#             y_pred.append(fc[0])
#             pred_upper.append(conf[0][1])
#             pred_lower.append(conf[0][0])
#             model.update(fc[0])
#     return pd.Series(y_pred, index=index), pred_upper, pred_lower


# # Forecast 
# fc, upper, lower = forecast(len(test_data), model_fit, test_data.index, data = test_data)

# # pandas series 생성
# # fc # 예측결과
# lower_series = pd.Series(lower, index=test_data.index)  # 예측결과의 하한 바운드
# upper_series = pd.Series(upper, index=test_data.index)  # 예측결과의 상한 바운드

# # Plot
# # plt.figure(figsize=(20,6))
# # plt.plot(train_data, label='train_data')
# # plt.plot(test_data, c='b', label='test_data (actual price)')
# # plt.plot(fc, c='r',label='predicted price')
# # plt.fill_between(lower_series.index, lower_series, upper_series, color='k', alpha=.10)
# # plt.legend(loc='upper left')
# # plt.show()



# # 향후 1년 주가 예측

# # 주식 개장일 불러오는 함수 생성
# import exchange_calendars as ecals
# def get_open_dates(start,end):
#     k = ecals.get_calendar("XKRX")
#     df = pd.DataFrame(k.schedule.loc[start:end]) #["2022-11-01":"2023-10-31"])
#     # print(df['open'])
#     date_list = []
#     for i in df['open']:
#         date_list.append(i.strftime("%Y-%m-%d"))
#        # print(i.strftime("%Y-%m-%d"))   
#     date_index = pd.DatetimeIndex(date_list)
#     return date_index  # DatetimeIndex

# # 향후 1년 주가 예측
# date_index = get_open_dates("2024-07-16","2025-07-16")
# fc2, upper2, lower2 = forecast(len(date_index), model_fit, date_index)
# print('1년 후 주가') 
# print(fc2.tail())
# # fc2, conf = forecast_n_step(model_fit, len(date_list))
# lower_series2 = pd.Series(lower2, index=date_index)  # 예측결과의 하한 바운드
# upper_series2 = pd.Series(upper2, index=date_index)  # 예측결과의 상한 바운드
# # plot
# plt.figure(figsize=(20,6))
# plt.plot(train_data, label='original')
# plt.plot(test_data, c='b', label='actual price')
# plt.plot(fc, c='r',label='predicted price')
# plt.plot(fc2, c='g',label='forward predicted price')
# plt.fill_between(lower_series.index, lower_series, upper_series, color='k', alpha=.10)
# plt.fill_between(lower_series2.index, lower_series2, upper_series2, color='k', alpha=.10)
# plt.title('After 1 year')
# plt.legend(loc='upper left')
# plt.show()
