# Real Baby RSA

This challenge gives us two files:

- `problem.py`, with the algorithm used to encrypt the flag;
- `output`, with the encrypted flag.

The algorithm is simple: the integer value of each character in the flag is multiplied _e = 65537_ times, and the result modulo _N_ is printed. Since the flag is encrypted one character at a time and _e_ and _N_ are known, it is easy to retrieve the flag.

First, we encrypt the characters that are likely to be in the flag and use the output as keys in a dictionary.

```python
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_{}'
dictionary = {}

for char in alphabet:
	dictionary[str(pow(ord(char), e, N))] = char
```

Now we retrieve the contents of `output` and use our dictionary to decrypt each line. Don't forget to `strip()` the input in order to remove the trailing `\n`.

```python
flag = ''

with open('output', 'r') as f:
	for line in f:
		flag += dictionary[str(line.strip())]

print(flag)
```

These simple steps give us the flag.

Flag: `TWCTF{padding_is_important}`
