f = open('flag.txt', 'r')

linhas = {}

x = f.readline()
for i in range(2, 13):
	linhas[i] = f.readline()

while len(linhas[2]) > 10:
	for i in range(2, 13):
		print(linhas[i][:20])
		linhas[i] = linhas[i][20:]

