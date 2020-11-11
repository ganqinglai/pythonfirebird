from handlers.login import LoginHandler, Showstudent4

url = [
    (r'/login', LoginHandler),
    (r'/show', Showstudent4),
]
