from handlers.user import RegisterHandler
from handlers.user import LoginHandler
from handlers.user import TestAuthHandler

url_patterns = [
    (r"/register", RegisterHandler),
    (r"/login", LoginHandler),
    (r"/test", TestAuthHandler)
]
