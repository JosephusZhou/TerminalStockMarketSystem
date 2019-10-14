#!/usr/bin/python3
import json
import re
import time

import requests


# 获取最新行情
def get_markets(res_list):
    new_list = []
    for res in res_list:
        new_list.append(get_market_info(res))
    return new_list


# 请求行情数据
def get_market_info(res):
    stock = {"code": res[0], "name": "", "cost_price": res[2], "current_price": "", "up_down": 0,
             "up_down_rate": "0.00", "shares_held": res[3]}
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }
    timestamp = str(int(round(time.time() * 1000)))
    token = "4f1862fc3b5e77c150a2b985b12db0fc"
    cb = "jQuery18307093346156478528_" + timestamp
    stock_id = res[0] + res[1]
    url = "http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token={token}&cb={cb}&id={" \
          "id}&type=k&authorityType=&_={timestamp} ".format(token=str(token),
                                                            cb=str(cb),
                                                            id=str(stock_id),
                                                            timestamp=str(timestamp)
                                                            )
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = loads_jsonp(response.text)
            stock["name"] = data['name']
            stock["current_price"] = data['info']["c"]
            stock = calculate_rate(stock)
        else:
            print('url: ' + url + ", code: " + response.status_code)
    except Exception as e:
        print(e)
    return stock


# 计算涨跌
def calculate_rate(stock):
    cost = float(stock["cost_price"])
    current = float(stock["current_price"])
    if cost > current:
        stock["up_down"] = -1
    elif cost < current:
        stock["up_down"] = 1
    stock["up_down_rate"] = (current - cost) / (cost * 1.0)
    return stock


# 加载 json
def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except Exception as e:
        print(e)
        return ""
