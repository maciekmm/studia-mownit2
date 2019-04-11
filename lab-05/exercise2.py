import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

my_img = Image.open('lena512.bmp').convert('L')
# Visualize the result
A = np.asarray(my_img)

u, s, vh = np.linalg.svd(my_img)
fig = plt.figure()
compressed = np.zeros(A.shape)
sub = 0
for i in range(min(A.shape[0], A.shape[1])):
    compressed += s[i] * np.outer(u.T[i], vh[i])
    print(np.linalg.norm(A-compressed))
    if i in [1, 5, 10, 20, 30, 40, 50, 100, 300]:
        sub += 1
        pane = fig.add_subplot(3, 3, sub)
        pane.imshow(compressed, cmap='gray', vmin=0, vmax=255)

fig.show()
plt.show()
