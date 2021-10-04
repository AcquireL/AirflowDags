import pymysql



class GetData:
    # 打开数据库连接
    # 注意：这里已经假定存在数据库testdb，db指定了连接的数据库，当然这个参数也可以没有
    db = pymysql.connect(host='192.168.124.6', port=3306, user='root', passwd='713181', db='test_db', charset='utf8')

    def getMaysqlVersion(self):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()

        # 使用execute方法执行SQL语句
        cursor.execute("SELECT VERSION()")

        # 使用 fetchone() 方法获取一条数据
        data = cursor.fetchone()

        print("Database version : %s " % data)

        # 关闭数据库连接
        self.db.close()


getData = GetData()
getData.getMaysqlVersion()