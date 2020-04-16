import time
import pymysql


def get_time():
    time_str = time.strftime('%Y{}%m{}%d{} %X')
    return time_str.format('年', '月', '日')


def get_conn():
    conn = pymysql.connect(host='xxx',
                      user='xx',
                      password='x',
                      db='xx')
    cursor = conn.cursor()  # 创建游标， 默认元组型
    return conn, cursor


def close_conn(conn, cursor):
    cursor.close()
    conn.close()


def query(sql, *args):
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res


def get_c1_data():
    sql = 'SELECT SUM(confirm),' \
          '(SELECT suspect FROM history ORDER BY ds DESC LIMIT 1),' \
          'SUM(heal),' \
          'SUM(dead) ' \
          'FROM details ' \
          'WHERE update_time=(SELECT update_time FROM details ORDER BY update_time DESC LIMIT 1)'
    res = query(sql)
    return res[0]


def get_c2_data():
    sql = 'SELECT province, SUM(confirm) FROM details ' \
          'WHERE update_time=(SELECT update_time FROM details ' \
          'ORDER BY update_time DESC LIMIT 1) ' \
          'GROUP BY province'
    res = query(sql)
    return res


def get_l1_data():
    sql = 'SELECT ds, confirm, suspect, heal, dead FROM history'
    res = query(sql)
    return res


def get_l2_data():
    sql = 'SELECT ds, confirm_add, suspect_add FROM history'
    res = query(sql)
    return res


def get_r1_data():
    sql = 'SELECT city, confirm FROM ' \
          '(SELECT city, confirm FROM details ' \
          'WHERE update_time=(SELECT update_time FROM details ORDER BY update_time DESC LIMIT 1)' \
          'AND province NOT IN ("湖北","北京","上海","天津","重庆")' \
          'UNION ALL ' \
          'SELECT province AS city, SUM(confirm) AS confirm FROM details ' \
          'WHERE update_time=(SELECT update_time FROM details ORDER BY update_time DESC LIMIT 1) ' \
          'AND province IN ("北京","上海","天津","重庆") GROUP BY province) AS a ' \
          'ORDER BY confirm DESC LIMIT 5'
    res = query(sql)
    return res


def get_r2_data():
    sql = 'SELECT content FROM hotsearch ORDER BY id DESC LIMIT 20'
    res = query(sql)
    return res


if __name__ == '__main__':
    print(get_l2_data())
