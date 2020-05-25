import pymssql
from qaconfig import DataConstant as dc

class MSSQL:

    def __init__(self):
        self._host = dc.mssql_db_host
        self._user = dc.mssql_db_user
        self._password = dc.mssql_db_password
        self._db = dc.mssql_db_dbname
        self._charset = dc.mssql_db_charset

    def _connect_db(self):
        self.conn = pymssql.connect(host=self._host, user=self._user, password=self._password, database=self._db,charset=self._charset)
        self.cursor = self.conn.cursor()
        if not self.cursor:
            raise (ConnectionError, "The connection to databse is fail")
        else:
            return self.cursor

    def fetch_one(self, query):
        try:
            cursor = self._connect_db()
            cursor.execute(query)
            db_result = self.cursor.fetchone()
            return db_result
        except Exception as e:
            raise (Exception, e)
        finally:
            self.conn.close()

    def fetch_all(self, query):
        try:
            cursor = self._connect_db()
            cursor.execute(query)
            db_result = self.cursor.fetchall()
            return db_result
        except Exception as e:
            raise (Exception, e)
        finally:
            self.conn.close()

    def execute_query(self, query):
        try:
            cursor = self._connect_db()
            cursor.execute(query)
            self.conn.commit()

        finally:
            self.conn.close()

    def insert_all(self, query):
        pass

