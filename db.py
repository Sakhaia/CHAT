from pymongo import MongoClient
import bcrypt

class Database:
    def __init__(self):
        self.client = MongoClient('mongodb+srv://test:test@chatapp.mv3ebhv.mongodb.net/?retryWrites=true&w=majority')
        self.db = self.client['users']
        self.users = self.db['user_data']

    def register_user(self, user_info):
        # Хеширование пароля перед сохранением
        hashed_password = bcrypt.hashpw(user_info['password'].encode('utf-8'), bcrypt.gensalt())
        user_info['password'] = hashed_password
        self.users.insert_one(user_info)

    def login_user(self, username, password):
        user = self.users.find_one({"username": username})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return True
        return False
    def user_exists(self, username):
        return self.users.find_one({"username": username}) is not None
