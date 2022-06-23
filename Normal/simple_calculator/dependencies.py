from itertools import combinations, permutations
from nameko.extensions import DependencyProvider
import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

from celery_task import prime,palindrome,isPrime

class DatabaseWrapper:
    def __init__(self):
        self.connection =  None
    def prime(self,n):
        result = [''.join(i) for i in prime(n)]
        return  result

    def palindrome(self,n):
        result = [''.join(i) for i in palindrome(n)]
        return  result

    def isPrime(self,n):
        result = isPrime(n)
        return  result

class Database(DependencyProvider):
    def __init__(self):
        try:
            self.connection = mysql.connector.pooling.MySQLConnectionPool(
                pool_name='mypool',
                pool_size=5,
                host='localhost',
                user='root',
                password='',
                database='simple_calculator'
            )
        except Error as msg:
            print("Error Database not Connected",msg)
    def get_dependency(self, worker_ctx):
        if self.connection is None:
            self.connection = DatabaseWrapper()
        return self.connection