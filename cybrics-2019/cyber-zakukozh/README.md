# Zakukozh

> Zakukozh (Cyber, Baby, 10 pts)
> Author: Khanov Artur (awengar)
> 
> This image containing flag is encrypted with affine cipher. Scrape it
> 
> zakukozh.bin

The description of the challenge tells us an image has been encrypted using the [affine cipher](https://en.wikipedia.org/wiki/Affine_cipher). This is a simple substitution cipher where each letter x is replaced by another one given by the formula _E(x) = (a × x) + b mod m_, where _x_ is the letter we're encrypting, _m_ is the size of the alphabet and _a, b_ are the keys of the cipher. _a_ and _m_ must be coprime.

Decryption is given by _D(x) = a^(-1) × (x - b) mod m_, where _a^(-1)_ is the multiplicative inverse of _a_. _b_ is the same for both functions.

In our case, _m_ = 256 because we're working with bytes instead of letters. Therefore, _a_ is an odd number between 3 and 255 (because 256 is a power of 2 and any even number would be divisible by 2). This actually means there are only 127 × 256 = 32512 possible key combinations, which is small enough to bruteforece.

Entering `file zakukozh.bin` on the console gives us no useful information. Taking a look at the `zakukozh.bin` file with an hex editor, we can see the header starts with `60 09 eb 82 1c ef df ef`. Let's analyze the header of common image formats to find similarities:

- JPEG: `ff d8 ff e0 xx xx 4a 46 49 46`
- GIF: `47 49 46 38 39 61`
- PNG: `89 50 4e 47 0d 0a 1a 0a`

The sixth and eighth bytes are identical in our file (`ef`) and in the PNG header (`0a`), suggesting the encrypted file is a PNG image. Knowing both ciphertext and cleartext, it's easy to find out _a_ and _b_ such that E(`0x89`) = `0x60`, E(`0x50`) = `0x09` and so on.

```python
png      = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]
zakukozh = [0x60, 0x09, 0xeb, 0x82, 0x1c, 0xef, 0xdf, 0xef]

for a in range(3, 256, 2):
  for b in range(0, 256):
    c = png[:]
    for i in range(0, len(c)):
      c[i] = ((a * c[i]) + b) % 256
    if c == zakukozh:
      print('a: %d b: %d' % (a, b))
```

This script gives us `a: 15 b: 89`. _b_ is the same for encryption and decryption, so we only need to find _a_.

```python
png      = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]
zakukozh = [0x60, 0x09, 0xeb, 0x82, 0x1c, 0xef, 0xdf, 0xef]
b = 89

for a in range(3, 256, 2):
  c = zakukozh[:]
  for i in range(0, len(c)):
    c[i] = (a * (c[i] - b)) % 256
  if c == png:
    print('a: %d b: %d' % (a, b))
```

This script gives us `a: 239 b: 89`. Now we can decrypt the whole file.

```python
with open('zakukozh.bin', 'rb') as f:
  content = f.read()
with open('output.png', 'wb') as f:
  for c in content:
    f.write(chr((239 * (ord(c) - 89)) % 256))
```

In the image we have the flag `cybrics{W311_C0M3_2_CY13R1C5}`.
