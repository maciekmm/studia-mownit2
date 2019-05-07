import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


def load_img(path):
    im = Image.open(path).convert('L')
    (width, height) = im.size
    greyscale_map = list(im.getdata())
    greyscale_map = np.array(greyscale_map)
    greyscale_map = greyscale_map.reshape((height, width))
    return 255 - greyscale_map


pattern = load_img('galia_e.png')
text = load_img('galia.png')

pattern_fft = np.fft.fft2(np.rot90(pattern, 2), text.shape)
text_fft = np.fft.fft2(text)

correlation = np.real(np.fft.ifft2(np.multiply(text_fft, pattern_fft)))

max = np.max(correlation)
threshold = max * 0.95
correlation[correlation < threshold] = 0
correlation[correlation >= threshold] = 1

print(len(np.transpose(np.nonzero(correlation))))

for es in np.transpose(np.nonzero(correlation)):
    for width in range(pattern.shape[0]):
        for height in range(pattern.shape[1]):
            correlation[es[0] - width, es[1] - height] = 1

print(np.max(text))

text[(correlation != 1) & (text > 0)] //= 3

# print(colorized)
# plt.subplot("211")
# plt.imshow(correlation, cmap='gray')
plt.subplot("111")
plt.imshow(text, cmap='gray')
plt.show()
