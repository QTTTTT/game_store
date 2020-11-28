
import pymysql
from config import config

def query(sql):
    """
    功能; 使用sql语句查询数据库.
    参数: sql(string)
    """
    db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], config['DATABASE_NAME'], charset='utf8')
    cur = db.cursor()
    try:
        cur.execute(sql)
        result = cur.fetchall()
        db.commit()

        #print('query success')

        # print('query success')
    except:
        # print('query loss')
        db.rollback()
    cur.close()
    db.close()
    return result


def update(sql):
    """
    功能; 使用sql语句更新数据库。
    参数: sql(string)
    """
    db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], config['DATABASE_NAME'], charset='utf8')
    cur = db.cursor()
    try:
        cur.execute(sql)
        db.commit()
        #print('update success')
        # print('update success')
    except:
        # print('update loss')
        db.rollback()
    cur.close()
    db.close()
