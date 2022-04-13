# prime function
def isPrime(num):
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                return False
        else:
            return True
    else:
        return False

def nth_prime_num(num):
    count = 0
    n = 1
    while count < num:
        n += 1
        if isPrime(n):
            count += 1
    return n

print(nth_prime_num(10));