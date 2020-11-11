import secrets
import string
import hashlib

m = hashlib.md5()
with open(r'D:/2.png', 'rb') as f:
    for line in f:
        m.update(line)
print(m.hexdigest())  # 47a6b079cc33a4f312786b46e61e0305

m = hashlib.md5()
with open(r'F:/2.png', 'rb') as f:
    for line in f:
        m.update(line)
print(m.hexdigest())

alphanum = string.ascii_letters + string.digits
password = ''.join(secrets.choice(alphanum) for i in range(4))
print(password)
