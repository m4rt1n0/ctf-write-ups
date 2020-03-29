# Dissolved

> Dissolved... Image... What does that even mean?!
> 
> stego.png

For steganography challenges, a good first step is to use [Stegsolve](https://github.com/zardus/ctf-tools) to find any odd patterns in the image. By carefully looking at each bitplane, we'll notice there are a few different pixels in bits 0 and 2 of the alpha channel.

The hypothesis is that the flag data is hidden in these pixels. To make it easier to manipulate and experiment, let's get those pixels in Python:

```python
from scipy import misc
arr = misc.imread('stego.png')

pixels = []

for i in range(0, len(arr)):
  for j in range(0, len(arr[0])):
    if arr[i, j, 3] != 255:
      pixels.append(arr[i, j])
```

The image is read as a multidimensional array, where `arr[5, 3, 0]` represents the red (`'RGBA'[0]`) value at position (3, 5). We copied to the `pixels` list every pixel where the alpha channel is not 255 (i.e. the weird pixels we found).

Let's analyze what we have: `len(pixels)` returns 312, which is divisible. by 8. Also, 312÷8 = 39, which is a reasonable size for a flag. Thus, each pixel might be hiding 1 bit of data, probably in the least significant bit (LSB). We don't know which channel contains the data, so let's get the LSB of each channel separately and see what we get:

```python
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
```

And here's the result:

```
Red:   JP±j£Ò
¹2íÞepF¼ 
NmüåÛ'÷ÏQÂ·ðA
Green: ?-Â`zHý5Ë¡Òø3òyE?&z¸%Ï*ÅÁÊ9QxØâ]PØßA
Blue:  VolgaCTF{Tr@nspar3ncy_g1ves_fLag_aw@y!}
```

Flag: `VolgaCTF{Tr@nspar3ncy_g1ves_fLag_aw@y!}`
