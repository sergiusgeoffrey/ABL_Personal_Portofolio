import json
import os
from flask import send_from_directory
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from werkzeug.wrappers import Response
from dependencies.session import SessionProvider


class GatewayService:
    name='gateway'
    rpce=RpcProxy('simple_cloud')
    session_provider = SessionProvider()

    @http('POST','/register')
    def register(self,request):
        data=json.loads(request.data)
        username=data['username']
        password=data['password']
        register=self.rpce.register(username,password)
        return Response(json.dumps(register),mimetype='application/json')
    
    @http('GET', '/login')
    def login(self, request):
        username=request.args.get('username')
        password=request.args.get('password')
        login=self.rpce.login(username,password)
        return Response(json.dumps(login),mimetype='application/json')
        
    @http('POST','/logout')
    def logout(self, request):
        cookies = request.cookies
        if cookies:
            confirm = self.session_provider.delete_session(cookies['SESSID'])
            if (confirm):
                result = Response('LOGOUT SUCCESS')
                result.delete_cookie('SESSID')
            else:
                result = Response("LOGOUT FAILED")
            return result
    
    @http("POST", "/upload")
    def upload(self, request):
        cookies = request.cookies
        if cookies:
            session_id = cookies['SESSID']
            if (session_id):
                data = format(request.get_data(as_text=True))
                array = data.split("&")
                for file in array:
                    str = file.split("=")
                    if str[0] == "filename":
                        filename = str[1]
                    if str[0] == "file":
                        file = str[1]
                file_upload = self.database.upload(filename, file)
                return json.dumps(file_upload)
            else:
                return Response("LOGIN REQUIRED")
        else:
            return Response("LOGIN REQUIRED")

    @http("GET", "/<string:namafile>")
    def download(self, request,namafile):
        cookies = request.cookies
        if cookies:
            session_id = cookies['SESSID']
            if (session_id):
                return send_from_directory(os.getcwd()+"/files", namafile)
            else:
                return Response("LOGIN REQUIRED")
        else:
            return Response("LOGIN REQUIRED")