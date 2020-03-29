# Noname

> I have Noname; I am but two days old.
> 
> encrypted encryptor.py

This challenge gives us two files:

- `encrypted`, with the encrypted flag;
- `encryptor.py`, with the code used to encrypt the flag.

The code in `encryptor.py` is very short; the cipher used is AES and the key is the MD5 digest of a timestamp (`time.time()`) with a precison of seconds (because of `int()`). Each day [usually](https://en.wikipedia.org/wiki/Leap_second) has 60×60×24 = 86400 seconds, and with the hint given in the description ("I am but two days old"), a brute force attack is feasible.

We'll start with the timestamp of the day of the challenge. In JavaScript, `new Date("2020-03-28").getTime()/1000` gives us 1585353600 (we want seconds, not milliseconds). We'll use the MD5 digest of this timestamp as the key to decrypt the flag.

```
timestamp = 1585353600
key = md5(str(timestamp)).digest()
aes = AES.new(key, AES.MODE_ECB)
outData = aes.decrypt(flag)
```

We expect the flag to start with `VolgaCTF{`. If there's no such pattern in the decrypted flag, we'll decrease the timestamp by 1 and repeat (by wrapping our code in a `while` loop); otherwise, we probably found our flag.

```
if 'volga' in outData.lower():
  print(str(timestamp) + ': ' + outData)
  break
timestamp = timestamp - 1
```

In a few seconds, we get our flag (along with some padding we didn't treat):

```
1585242915: VolgaCTF{5om3tim3s_8rutf0rc3_i5_th3_345iest_w4y}
```

Flag: `VolgaCTF{5om3tim3s_8rutf0rc3_i5_th3_345iest_w4y}`
