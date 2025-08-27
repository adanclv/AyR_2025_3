from keras.utils import load_img

largo, alto = 300, 200

file = "../../Archivos/Images/airplane1.jpeg"

img = load_img(file, target_size = (largo, alto)
               , color_mode ="grayscale"
               )

print(img.size)
print(img.mode)

import matplotlib.pyplot as plt
plt.imshow(img, cmap='gray')
plt.imshow(img)
plt.xticks([])
plt.yticks([])
plt.show()
