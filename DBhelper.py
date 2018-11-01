import mysql.connector


class DBhelper:
    __cnx_kwargs = {
        'host': "192.168.10.53",
        'user': "mysql",
        'password': "password",
        'database': "ntest",
        'port': 3306,
        'charset': 'utf8',
    }
    __conn = None

    def conn(self):
        if self.__conn is not None:
            return self.__conn
        self.__conn = mysql.connector.connect(**self.__cnx_kwargs)
        return self.__conn

    def update(self, sql, args=()):
        update_count, cursor = 0, None
        try:
            cursor = self.conn().cursor()
            cursor.execute(sql, args)
            update_count = cursor.rowcount
            self.__conn.commit()
        except mysql.connector.DatabaseError as e:
            print('update error!{}'.format(e))
            self.__conn.rollback()
        finally:
            cursor.close()
        return update_count

    def query(self, sql, args=()):
        cursor, value = None, None
        try:
            cursor = self.conn().cursor()
            cursor.execute(sql, args)
            value = cursor.fetchall()
        except mysql.connector.DatabaseError as e:
            print('query error!{}'.format(e))
        finally:
            cursor.close()
        return value

    def query_one(self, sql, args=()):
        cursor, value = None, None
        try:
            cursor = self.conn().cursor()
            cursor.execute(sql, args)
            value = cursor.fetchone()
        except mysql.connector.DatabaseError as e:
            print('query error!{}'.format(e))
        finally:
            cursor.close()
        return value


if __name__ == "__main__":
    dbhelper = DBhelper()
    print(dir(dbhelper))
    # novels = dbhelper.query("select * from novel limit 10")
    chapters = dbhelper.query_one("select id from novel where sourceId = 20424")
    # print(novels)
    print(type(chapters[0]))
