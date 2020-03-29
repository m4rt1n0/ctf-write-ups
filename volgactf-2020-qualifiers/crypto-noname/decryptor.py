from Crypto.Cipher import AES
import time
from hashlib import md5

with open('encrypted') as f:
  flag = f.read().decode('base64')

# 2020-03-28 = 1585353600
# key = 1585242915

timestamp = 1585353600

while True:
  key = md5(str(timestamp)).digest()
  aes = AES.new(key, AES.MODE_ECB)
  outData = aes.decrypt(flag)
  if 'volga' in outData.lower():
    print(str(timestamp) + ': ' + outData)
    break
  timestamp = timestamp - 1
