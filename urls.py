from handlers.user import RegisterHandler, LoginHandler, LogoutHandler
from handlers.generic import GenericHandler

url_patterns = [
    (r"/register", RegisterHandler),
    (r"/login", LoginHandler),
    (r"/api/(?P<cls>[^\/]+)/?(?P<slug>[^\/]+)?/", GenericHandler),
]
