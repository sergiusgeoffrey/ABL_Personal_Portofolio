import json
from nameko.rpc import RpcProxy
from nameko.web.handlers import http

class GatewayService:
    name = 'gateway'
    
    prime_service = RpcProxy('prime_service')

    @http('GET', '/api/prime/<int:number>')
    def prime(self, number):
        result = self.database.prime(number)
        return json.dumps({'result': result})

    @http('GET', '/api/prime/palindrome/<int:number>')
    def palindrome(self, number):
        result = self.database.palindrome(number)
        return json.dumps({'result': result})
