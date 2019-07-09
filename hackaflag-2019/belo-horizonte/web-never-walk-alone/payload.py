def readfile(filename):
	output = ''
	with open(filename, 'rb') as f:
		byte = f.read(1)
		while byte != '':
			output += '{:02x}'.format(ord(byte))
			byte = f.read(1)
	return output

str1 = readfile('sha1_1.html')
str2 = readfile('sha1_2.html')

str1fmt = ''.join(['%' + str1[i] + str1[i + 1] for i in range(0, len(str1)) if i % 2 == 0])
str2fmt = ''.join(['%' + str2[i] + str2[i + 1] for i in range(0, len(str2)) if i % 2 == 0])

url = 'http://68.183.31.62:33332/350208e449a15d3ca155db335ae219b9.php'

print(url + '?u=' + str1fmt + '&x=' + str2fmt)