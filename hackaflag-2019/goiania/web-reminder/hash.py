import sys
import hashlib

if len(sys.argv) < 2:
	print('Missing argument')

for i in range(1, 1000000):
	m = hashlib.md5()
	m.update(str(i).encode('utf-8'))
	h = m.hexdigest()[:4]
	if h == sys.argv[1][:4]:
		print(str(i) + ' - ' + h)
		break