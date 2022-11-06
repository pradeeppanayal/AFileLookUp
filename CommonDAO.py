import sqlite3


class CommonDAO(object):
    def __init__(self,dbname:str) -> None:    
        self.dbname = dbname

    def _executeSingle(self, sql) -> any:
        conn = sqlite3.connect(self.dbname)    
        result = conn.execute(sql)
        val = result.fetchone()
        if(val):
            val = val[0]
        conn.close()
        return val

    def _executeUpdate(self, sql) -> int:
        conn = sqlite3.connect(self.dbname)    
        result = conn.execute(sql)
        count = result.rowcount
        conn.commit()
        conn.close()
        return count

    def _executeFetchAll(self,sql:str) -> list:
        conn = sqlite3.connect(self.dbname)   
        cursor = conn.execute(sql)
        items = cursor.fetchall()
        conn.close()
        return items