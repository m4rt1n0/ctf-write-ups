#!/usr/bin/python
import sys, hashlib, random, itertools, string, re

if len(sys.argv) <= 4 or (sys.argv[1] != "enc" and sys.argv[1] != "dec"):
    print "USAGE:"
    print "%s {enc|dec} key input.txt output.txt"%sys.argv[0]
    exit(1)

_, mode, key, inputFile, outputFile = sys.argv

## initialize the alphabet permutation
key = hashlib.sha256(key).hexdigest()
random.seed(int(key, 16))

## shuffle the monogram mapping
plain1 = list(string.ascii_lowercase)
crypt1 = plain1[:]
random.shuffle(crypt1)

## shuffle the bigram mapping
plain2 = [''.join(x) for x in itertools.product(string.ascii_lowercase, string.ascii_lowercase)]
crypt2 = plain2[:]
random.shuffle(crypt2)

## if decrypting, replace in the other direction
if mode == "dec":
    plain1, crypt1 = crypt1, plain1
    plain2, crypt2 = crypt2, plain2

map1 = dict(zip(plain1, crypt1))
map2 = dict(zip(plain2, crypt2))

def transform(s):
    s = s.group(0)
    res = ""
    for i in range(0, len(s), 2):
        chunk = s[i:i+2]
        if len(chunk) == 2:  ## if it's a bigram
            ciph = map2[chunk.lower()]
            if chunk[0] == chunk[0].upper():
                ciph = ciph[0].upper() + ciph[1]
            if chunk[1] == chunk[1].upper():
                ciph = ciph[0] + ciph[1].upper()
        elif len(chunk) == 1:  ## if it's last odd character
            ciph = map1[chunk.lower()]
            if chunk == chunk.upper():
                ciph = ciph.upper()
        res += ciph
    return res

## actually transform the text
text = open(sys.argv[3], "rb").read()
text = re.sub(r'[a-z]+', transform, text, 0, re.I)
open(sys.argv[4], "wb").write(text)
