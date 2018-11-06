import pymysql.cursors


class DBhelper:
    # __cnx_kwargs = {
    #     'host': "192.168.10.53",
    #     'user': "mysql",
    #     'password': "password",
    #     'database': "ntest",
    #     'port': 3306,
    #     'charset': 'utf8',
    # }
    __cnx_kwargs = {
        'host': "localhost",
        'user': "root",
        'password': "zdddmysql",
        'database': "novels",
        'port': 3306,
        'charset': 'utf8',
    }
    __conn = None

    def conn(self):
        if self.__conn is not None:
            return self.__conn
        self.__conn = pymysql.connect(**self.__cnx_kwargs)
        return self.__conn

    def update(self, sql, args=()):
        update_count, cursor = 0, None
        try:
            cursor = self.conn().cursor()
            cursor.execute(sql, args)
            update_count = cursor.rowcount
            self.__conn.commit()
            print(sql % args)
        except pymysql.err.DatabaseError as e:
            print('update error!{}'.format(e))
            self.__conn.rollback()
            raise e
        finally:
            cursor.close()
        return update_count

    def query(self, sql, args=()):
        cursor, value = None, None
        try:
            cursor = self.conn().cursor()
            cursor.execute(sql, args)
            value = cursor.fetchall()
            print(sql % args)
        except pymysql.err.DatabaseError as e:
            print('query error!{}'.format(e))
            raise e
        finally:
            cursor.close()
        return value

    def query_one(self, sql, args=()):
        cursor, value = None, None
        try:
            cursor = self.conn().cursor()
            cursor.execute(sql, args)
            value = cursor.fetchone()
            print(sql % args)
        except pymysql.err.DatabaseError as e:
            print('query error!{}'.format(e))
            raise e
        finally:
            cursor.close()
        return value


if __name__ == "__main__":
    dbhelper = DBhelper()
    # novels = dbhelper.query("select * from novel limit 10")
    chapters = dbhelper.query("select id from novel limit 10")
    print(chapters)
    print(chapters[0][0])
