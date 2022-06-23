from nameko.rpc import rpc
import dependencies
import gateway

class PrimeService:
    name = 'prime_service'
    gateway = gateway.Gateway()
    dependencies = [dependencies.RedisClient]

    @rpc
    def is_prime(self, num):
        return self.gateway.is_prime(num)

    @rpc
    def prime(self, num):
        return self.gateway.prime(num)

    @rpc
    def palindrome(self, num):
        return self.gateway.palindrome(num)