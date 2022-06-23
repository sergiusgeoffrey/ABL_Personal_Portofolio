from unicodedata import name
from nameko.rpc import rpc
import dependencies.dependencies as database

class CloudService:
    name='cloud_service'
    database=database.DatabaseProvider()

    @rpc
    def register(self,username,password):
        register=self.database.register(username,password)
        return register
    
    @rpc
    def login(self,username,password):
        login=self.database.login(username,password)
        return login

    @rpc
    def logout(self):
        logout=self.database.logout()
        return logout

    @rpc
    def upload(self,filename,file):
        upload=self.database.upload(filename,file)
        return upload
    
    @rpc
    def download(self,filename):
        download=self.database.download(filename)
        return download