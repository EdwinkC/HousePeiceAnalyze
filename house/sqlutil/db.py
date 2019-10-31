import pymysql

class MysqlDB:

    def __init__(self, host='127.0.0.1', user='root', pwd='root', db='test'):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.conn = None
        self.cursor = None

    # 建立连接
    def connectDB(self):
        try:
            self.conn = pymysql.connect(self.host, self.user, self.pwd, self.db, charset='utf8')
            self.cursor = self.conn.cursor()
            print('open connection!')
        except:
            print('connection fail!')

    # 关闭连接
    def close(self):
        if self.conn and self.cursor:
            self.cursor.close()
            self.conn.close()
        print('close connection!')

    # execute 增删改
    def execute(self, sql, param=None):
        try:
            self.cursor.execute(sql, param)
            self.conn.commit()
            print('execute sccess!')
        except:
            self.conn.rollback()
            print('execute fail!')

    # fetchall 查询
    def fetchall(self, sql, param=None):
        self.cursor.execute(sql, param)
        return self.cursor.fetchall()

if __name__ == '__main__':
    mydb = MysqlDB(user='root', pwd='123456', db='house')
    mydb.connectDB()

    result = mydb.fetchall('select distinct name from newdata')
    # result = mydb.fetchall('select * from dept limit 0, 1')
    for r in result:
        # for l in r:
        #     print(l)
        print(r[0])

    # mydb.execute("insert into dept (deptno, dname, loc) values(70, 'Tom', 'ShangHai')")
    # mydb.execute("delete from dept where deptno='70'")
    # mydb.execute("update dept set dname='Jhon' where deptno=70")

    mydb.close()