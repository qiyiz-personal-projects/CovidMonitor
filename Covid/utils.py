import time
import pymysql

def get_conn():
    """
    :return: 连接，游标
    """
    # 创建连接
    # conn = pymysql.connect(host="127.0.0.1",
    #                        user="root",
    #                        password="zhangqiyi1998",
    #                        db="covid",
    #                        charset="utf8")
    conn = pymysql.connect(host="rm-bp1a79us1g4479yaaro.mysql.rds.aliyuncs.com",
                           user="user0",
                           password="zqy261725@",
                           db="covid",
                           charset="utf8")
    # 创建游标
    cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def query(sql, *args):
    '''
    封装通用查询
    :param sql:
    :param args:
    :return: 返回查询到的结果，((), (),)的形式
    '''
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res

def get_c1_data():
    '''
    :return: 返回大屏div id=c1的数据 全国累计确诊地图
    '''
    # 因为会更新多次数据，取时间戳最新的那组数据(累计确诊，剩余疑似，累计治愈，累计死亡)
    sql = "select sum(confirm)," \
          "(select suspect from history order by ds desc limit 1)," \
          "sum(heal)," \
          "sum(dead) " \
          "from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) "
    res = query(sql)
    return res[0]

def get_c2_data():
    """
    :return: 返回各省数据
    """
    # 因为会更新多次数据，取时间戳最新的那组数据
    sql = "select province,sum(confirm) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    res = query(sql)
    return res


def get_l1_data():
    """
    :return: 返回历史数据用来分析全国累计趋势
    """
    sql = "select ds,confirm,suspect,heal,dead from history"
    res = query(sql)
    return res


def get_l2_data():
    """
    :return: 返回历史数据用来分析全国新增趋势
    """
    sql = "select ds,confirm_add,suspect_add from history"
    res = query(sql)
    return res


def get_r1_data():
    """
    :return:  返回全国新增病理数量top5
    """
    # 返回非湖北地区城市确诊人数前5名
    # sql = 'select city,confirm from' \
    #       '(select city,confirm from details'\
    #       'where update_time=(select update_time from details order by update_time desc limit 1)'\
    #       'and province not in ("湖北","北京","上海","天津","重庆")'\
    #       'union all'\
    #       'select province as city, sum(confirm) as confirm from details'\
    #       'where update_time=(select update_time from details order by update_time desc limit 1)'\
    #       'and province in ("北京","上海","天津","重庆") group by province) as a'\
    #       'order by confirm desc limit 5'

    sql = 'SELECT province,confirm_add FROM ' \
          '(select province,sum(confirm_add) as confirm_add from details  ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'group by province) as a ' \
          'ORDER BY confirm_add DESC LIMIT 5'

    res = query(sql)
    return res


def get_r2_data():
    '''
       :return: 今日新增病例地图
   '''
    # 因为会更新多次数据，取时间戳最新的那组数据
    sql = "select province,sum(confirm_add) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    res = query(sql)
    return res


def get_time():
    time_str = time.strftime("%Y{} %m{} %d{} %X")
    return time_str.format("年","月","日")


# if __name__ == "__main__":
    # 测试代码
    # print(get_time())
    # print(get_c1_data())
    # print(get_l1_data())
    # print(get_r1_data())
    # print(get_r2_data())