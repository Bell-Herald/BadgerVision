import random
import sys
import time
import hmac
import hashlib


the_iat = str(time.time())
the_exp = str(time.time() + 60 * 60 * 2)
header = """{
  "alg": "HS256",
  "typ": "JWT"
}"""

payload = """{
  "app_key": "YLfqZ1zkO5UCcVBhuqKcYzXUZunSp5ZbKg3q",
  "role_type": 1,
  "tpc": "oYO7shH2XAk6X8hllehPI3VX74k45676Fl4t",
  "version": 1,
  "iat": {the_iat},
  "exp": {the_exp}
}"""

"""signature = hmac.new(
    bytes(header, 'latin-1'),
     msg=bytes(payload, 'latin-1'),
     digestmod=hashlib.sha256
).hexdigest().upper()
"""

signature = hmac.new(
    key=bytes(header, 'latin-1'), 
    msg=bytes(payload, 'latin-1'), 
    digestmod=hashlib.sha256
).hexdigest().upper()


print("header", header)
print("payload", payload)
print("signature", signature)