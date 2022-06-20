# from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('calculator_service',backend='rpc:',broker='pyamqp://guest@localhost//')
    
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
def nth_prime_num(num):
    count = 0
    n = 1
    while count < num:
        n += 1
        if isPrime(n):
            count += 1
    return n

@app.task
def palindrome_prime(num):
    count = 0
    n = 1
    while count < num:
        n += 1
        if isPrime(n):
            if str(n) == str(n)[::-1]:
                count += 1
    return n

print("Input a number:",end=" ")
input = int(input())
print(nth_prime_num(input))
print(palindrome_prime(input))

#celery -A <file name here>  worker -l info -P eventlet --concurrency=1