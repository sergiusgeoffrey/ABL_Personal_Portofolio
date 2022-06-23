from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
app = Celery('app',
            backend='redis://6379/0',
            broker='pyamqp://guest@localhost//',)

@app.task
def isPrime(num):
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                return False
        else:
            return True
    else:
        return False

@app.task
def prime(num):
    count = 0
    n = 1
    while count < num:
        n += 1
        if isPrime(n):
            count += 1
    return n

@app.task
def palindrome(num):
    count = 0
    n = 1
    while count < num:
        n += 1
        if isPrime(n):
            if str(n) == str(n)[::-1]:
                count += 1
    return n