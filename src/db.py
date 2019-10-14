#!/usr/bin/python3
import os
import sqlite3


# 初始化 db 连接，并判断是否初始化数据表
def init_conn():
    if not os.path.exists('../db'):
        os.mkdir('../db')
    conn = sqlite3.connect('../db/stock.db')
    # create db
    cursor = conn.cursor()
    cursor.execute(
        "select count(*) from sqlite_master where type = 'table' and name = 'stock_info'")
    if cursor.fetchall()[0][0] == 0:
        cursor.execute('''create table stock_info(
        stock_code varchar primary key not null,
        market varchar not null,
        cost_price varchar not null,
        shares_held varchar not null)
        ''')
        conn.commit()
    cursor.close()
    return conn


# 关闭 db 连接
def close_conn(conn):
    conn.close()


# 读取所有数据
def query_data(conn):
    cursor = conn.cursor()
    cursor.execute("select * from stock_info")
    conn.commit()
    res_list = cursor.fetchall()
    cursor.close()
    return res_list


# 插入数据
def insert_data(conn, data):
    cursor = conn.cursor()
    sql_str = '''insert into stock_info (stock_code, market, cost_price, shares_held) values (
    '{code}', '{market}', '{price}', '{held}')'''.format(code=data["stock_code"],
                                                         market=data["market"],
                                                         price=data["cost_price"],
                                                         held=data["shares_held"])
    cursor.execute(sql_str)
    conn.commit()
    cursor.close()
