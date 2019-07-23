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
