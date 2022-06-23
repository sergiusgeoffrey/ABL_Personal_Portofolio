import uuid
import redis
from nameko.extensions import DependencyProvider
import pickle

class SessionWrapper:
    
    def __init__(self, connection):
        self.redis = connection
        self.default_expire = 60 * 60
    
    def generate_session_id(self):
        key = str(uuid.uuid4())
        return key

    def set_session(self, user_data):
        user_data_pickled = pickle.dumps(user_data)
        session_id = self.generate_session_id()
        self.redis.set(session_id, user_data_pickled, ex=self.default_expire)
        return session_id
    
    def get_session(self, session_id):
        result = self.redis.get(session_id)

        if result:
            user_data = pickle.loads(result)
        else:
            user_data = None

        return user_data
    
    def delete_session(self, session_id):
        result = self.redis.get(session_id)
        if result:
            self.redis.delete(session_id)
            return True
        else:
            return False

class SessionProvider(DependencyProvider):
    def setup(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0)
    
    def get_dependency(self, worker_ctx):
        return SessionWrapper(self.client)