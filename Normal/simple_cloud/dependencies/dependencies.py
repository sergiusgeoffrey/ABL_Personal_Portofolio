from nameko.extensions import DependencyProvider
import mysql.connector
from mysql.connector import Error
import mysql.connector.pooling

class DatabaseWrapper:
    connection = None

    def __init__(self, connection):
        self.connection = connection
    
    def register(self,username,password):
        try:
            cursor=self.connection.cursor(dictionary=True,buffered=True)
            query="SELECT * FROM user where username = '{}'".format(username)
            cursor.execute(query)
            if(cursor.rowcount > 0):
                return "Account Already Exist"
            else:
                query="INSERT INTO user (username,password) VALUES ('{}','{}')".format(username,password)
                cursor.execute(query)
                self.connection.commit()
                return "Account Created"
        except Error as e:
            print("Error Register",e)
            return False

    def login(self,username,password):
        try:
            cursor=self.connection.cursor(dictionary=True,buffered=True)
            query="SELECT * FROM user where username = '{}'".format(username)
            cursor.execute(query)
            if(cursor.rowcount == 0):
                cursor.close()
                return "Account Not Found"
            else:
                row=cursor.fetchone()
                if(row['password'] == password):
                    return True
                else:
                    return False
        except Error as e:
            print("Error Login",e)
            return False



class DatabaseProvider(DependencyProvider):

    connection_pool = None

    def setup(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=32,
                pool_reset_session=True,
                host='127.0.0.1',
                database='cloud_storage_db',
                user='root',
                password=''
            )
        except Error as e:
            print("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())