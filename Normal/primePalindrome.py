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

def palindrome_prime(num):
    count = 0
    n = 1
    while count < num:
        n += 1
        if isPrime(n):
            if str(n) == str(n)[::-1]:
                count += 1
    return n

print(palindrome_prime(10));