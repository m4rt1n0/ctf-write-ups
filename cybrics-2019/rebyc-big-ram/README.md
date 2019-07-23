# Big RAM

> Big RAM (rebyC, Easy, 117 pts)
> Author: Vlad Roskov (vos)
> 
> We heard that substitution ciphers are easy to crack with frequency analysis. Especially for English texts! This one, however, doesn’t map same letters to same letters, so it should be unbreakable.
> 
> We even encrypted an entire book with it. Inside this book, we keep the flag.
> 
> bigram.zip

This challenge gives us a `bigram.zip` file containing two other files:

- `encoder_decoder.py`: a Python script for encoding and decoding text
- `book.enc`: an encoded ebook with the flag somewhere in it

The cipher in `encoder_decoder.py` only encodes uppercase and lowercase letters, ignoring numbers and punctuation. Searching `book.enc` for `{` or `}`, we easily spot `xanjtou{sw_p_aqws_oefnehyh_jyiq_zw_qczoa_ybwrgzsbmu}`, which is our encoded flag.

A substitution cipher is easy to break if you have a sufficiently large piece of ciphertext. To break such a cipher, we use [frequency analysis](https://en.wikipedia.org/wiki/Frequency_analysis), which is based on the fact that some letters in a language appear more often than other letters. The letter "e", for example, appears 17 times in this sentence, while the letter "a" only appears 6 times. If the ciphertext is large enough, the frequency of each letter will be close to their frequency in the whole language.

The twist in this challenge is that, instead of individual letters, the idea was applied to pairs of letters, or bigrams, hence the name of the challenge. This makes things a bit more complicated, as we go from 26 possible letters to (26 × 26) + 26 = 702 possible "letters", which makes frequencies more evenly distributed.

First, we need the frequency of the most common bigrams in the English language. The list from the [bigram article](https://en.wikipedia.org/wiki/Bigram) on Wikipedia shall do.

```
th 1.52       en 0.55       ng 0.18
he 1.28       ed 0.53       of 0.16
in 0.94       to 0.52       al 0.09
er 0.94       it 0.50       de 0.09
an 0.82       ou 0.50       se 0.08
re 0.68       ea 0.47       le 0.08
nd 0.63       hi 0.46       sa 0.06
at 0.59       is 0.46       si 0.05
on 0.57       or 0.43       ar 0.04
nt 0.56       ti 0.34       ve 0.04
ha 0.56       as 0.33       ra 0.04
es 0.56       te 0.27       ld 0.02
st 0.55       et 0.19       ur 0.02
```

Now we need the frequency of the bigrams in the encoded book. We can piggyback on the provided code by adding a `freq = {}` dictionary and modifying the `transform` function a little bit:

```python
def transform(s):
    s = s.group(0)
    res = ""
    for i in range(0, len(s), 2):
        chunk = s[i:i+2]
		# add this if-else
        if chunk.lower() not in freq:
            freq[chunk.lower()] = 1
        else:
            freq[chunk.lower()] += 1
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
```

Now let's add some code to output the frequencies we've obtained:

```python
out = open('freq.txt', "wb")
for item in sorted(freq.items(), key=lambda x: x[1], reverse=True):
    out.write('%s, %d\n' % (item[0], item[1]))
```

Saving it as `freq.py`, we can now run `python freq.py enc anypassword book.enc freq.txt`. Instead of encoding `book.enc` again, the code will create a `freq.txt` file containing the frequency of each bigram in `book.enc`, sorted from higher to lower frequency. The beginning of the file should look like this:

```
yb, 12610
n, 11822
x, 7827
s, 7262
u, 6012
ow, 5406
wr, 5119
jo, 3736
jy, 3726
cd, 3615
xq, 3463
zv, 3088
by, 3064
a, 2990
d, 2988
cz, 2865
kt, 2626
jd, 2575
f, 2462
l, 2435
```

Rightaway we notice the frequency of `yb` is much higher than the other bigrams, just like `th` in the English language, so `yb` probably is `th` encoded. 

If we simply keep replacing encoded bigrams by their corresponding decoded bigrams, we'll have a problem: how will we know if a `th` in the encoded text is an encoded bigram or a decoded `yb`? To make things a bit easier, let's do one more trick:

1. run `python encoder_decoder.py enc anypassword book.enc book2.enc` to encode `book.enc` with `anypassword`;
2. open `encoder_decoder.py` and change `res += ciph` to `res += '[' + ciph + ']'`;
3. run `python encoder_decoder.py dec anypassword book2.enc bookbrackets.enc` to decode `book2.enc` with `anypassword`.

Here's the beginning of `bookbrackets.enc`:

```
[Gu][kc][uo] [Zj][wr][gm][xq][n] [Oe][fd][rc][sq][cz][u] [oe][uq][ol][s]: [Co][cm][pn][l] [am][zi][to] [xa][ej][vt][qs][v] [zp][xx] 2005.

[Sb][aj][wr][un][a] [Uc][yr][of][bu][l]
[Kg][ho][by][u]. [Xh][rh][uo][zo] [hs][mu]
[Ej][ld]-[ex][lo][vp][l]

[Wr][f] [jy][te][hd][qc][yt][n] [sd] [yb][n] [zv][hs][uq] [sd] [yb][n] [ad][ex][g] [aq][yb] [jy][sb] [pr][xg][uo] [wr][x] [re][ef][xw][g] [uc][of][gi][zo][lo] [sv][ac][xu] [ej] [xh][ea][tj][by][cd] [d] [lp][zw][by]'[u] [da][dk][vp][l] [wr][x] [jy][iq][by] [xh][io][in][yk][jy].
```

By encoding and decoding `book.enc` with the same password, we essentially have the same file, but now there are brackets around each encoded bigram, making it easier to distinguish bigrams and to keep track of the ones we haven't decoded yet.

Instead of relying on a text editor's "Find and replace", let's create a script called `replace.py` to decode the bigrams we know.

```python
import re

decodelist = [
  ('yb', 'th')
]

content = open('bookbrackets.enc', 'r').read()
for i in decodelist:
  content = re.sub('\[' + i[0] + '\]', i[1], content, 0, re.I)
print(content)
```

This way, we can keep expanding `decodelist` with new findings. We know the encoded flag is `xanjtou{sw_p_aqws_oefnehyh_jyiq_zw_qczoa_ybwrgzsbmu}`, so we can deduce `xantjou` is `cybrics` and add `('xa', 'cy'), ('nt', 'br'), ('jo', 'ic'), ('u', 's')` tuples to `decodelist`. Decoded bigrams have their surrounding brackets removed.

This part involves a lot of guessing. There are many `th[n]` in the encoded text, so `[n]` probably is `e`. There's `[lp][zw][by]'[u]`, so `[u]` might be `s` or `t`. By going back and forth between known and unknown bigrams, we can slowly make some progress. There will be mistakes, so it's important to check carefully each addition to the list. We can also focus on the bigrams of the flag (`sw`, `p`, `aq`, `ws` and so on), which are the ones that really matter for the challenge. This part feels like a letter-based sudoku and surprisingly I had quite some fun doing this, despite being a bit too slow for a CTF competition.

Although it did not occur to me at the time of the challenge, we can also use the frequency of whole words to help us decode bigrams. With this small `wordfreq.py` script, we can count the frequency of the encoded words and write them to `wordfreq.txt`:

```python
import re

content = open('book.enc', 'r').read().lower()
wordlist = re.sub('[^a-z ]*', '', content, 0).split()

wordfreq = {}

for word in wordlist:
  if word not in wordfreq:
    wordfreq[word] = 1
  else:
    wordfreq[word] += 1

out = open('wordfreq.txt', "wb")
for item in sorted(wordfreq.items(), key=lambda x: x[1], reverse=True):
    out.write('%s, %d\n' % (item[0], item[1]))
```

Here are the first 20 words:

```
ybn, 6551
wrx, 2894
jo, 2685
d, 2429
sd, 2015
ow, 1672
ijq, 1498
ads, 1416
kiu, 1224
zv, 1211
ezu, 1205
ybxq, 1021
p, 926
aqyb, 918
zw, 910
ufqbs, 838
od, 806
cz, 802
nca, 800
xq, 740

```

We can compare the results against [lists of the most common words in English](https://en.wikipedia.org/wiki/Most_common_words_in_English). Once again, there are many similarities between the two lists. There are, however, a few red herrings: `ufqbs`, for example, is the name of one of the characters of the book, so it definitely won't appear in the other list.

After about 100 decoded bigrams, it should be possible to decode the flag: `cybrics{ok_i_will_probably_read_it_later_thanksalot}`.

