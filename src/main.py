#!/usr/bin/python3

import db
import format
import spider
from prettytable import PrettyTable

#################################################
# 主程序，持续运行，动态获取行情以供查阅，也可以添加自选 #
#################################################

conn = None


# 主函数
def main():
    global conn
    print("欢迎进入{s}".format(s=format.format_light_content("终端股票行情系统")))
    # 打开 db 连接
    conn = db.init_conn()
    # 展示菜单
    menu()
    # 关闭 db 连接
    db.close_conn(conn)
    print("拜拜{s}".format(s=format.format_light_content("~")))


# 菜单
def menu():
    while True:
        s = "请选择:\n1. 当前行情\n2. 添加股票\n3. 退出\n"
        index = int(input(s))
        if index == 1:
            show_current_market()
        elif index == 2:
            add_new_stock()
        else:
            break


# 显示行情
def show_current_market():
    global conn
    res_list = db.query_data(conn)
    res_list = spider.get_markets(res_list)
    table = PrettyTable(["代码", "名称", "成本价", "现价", "涨跌幅", "持有份额"])
    for stock in res_list:
        table.add_row([stock["code"], stock["name"], stock["cost_price"],
                       format.format_up_down_content(stock["up_down"], stock["current_price"]),
                       format.format_up_down_content(stock["up_down"],
                                                     "{:.2%}".format(stock["up_down_rate"])),
                       stock["shares_held"]])
    print(table)


# 添加新股
def add_new_stock():
    global conn
    data = {"stock_code": (input("请输入股票代码:\n")),
            "market": (input("请输入股票市场(沪A为1，深A为2):\n")),
            "cost_price": str(input("请输入成本价:\n")),
            "shares_held": str(input("请输入持有份额:\n"))}
    db.insert_data(conn, data)
    print(format.format_light_content("添加成功."))


# 程序入口
main()
