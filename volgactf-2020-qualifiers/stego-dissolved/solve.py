from scipy import misc
arr = misc.imread('stego.png')

pixels = []

for i in range(0, len(arr)):
  for j in range(0, len(arr[0])):
    if arr[i, j, 3] != 255:
      pixels.append(arr[i, j])

r_bitstream = ''
g_bitstream = ''
b_bitstream = ''

for x in pixels:
  r_bitstream += str(x[0] & 1)
  g_bitstream += str(x[1] & 1)
  b_bitstream += str(x[2] & 1)

print('Red:   ' + ''.join(chr(int(r_bitstream[i*8:i*8+8],2)) for i in range(len(r_bitstream)//8)))
print('Green: ' + ''.join(chr(int(g_bitstream[i*8:i*8+8],2)) for i in range(len(g_bitstream)//8)))
print('Blue:  ' + ''.join(chr(int(b_bitstream[i*8:i*8+8],2)) for i in range(len(b_bitstream)//8)))
