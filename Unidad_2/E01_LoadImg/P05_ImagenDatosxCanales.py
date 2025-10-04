from keras.utils import load_img, img_to_array

largo, alto = 300, 200

file = "../../Archivos/Images/airplane1.jpeg"

img = load_img(file, target_size = (largo, alto)
               #, color_mode ="grayscale"
               )

print(img.size)
print(img.mode)

canal = 0
# canal = 1
# canal = 2
imagen_en_array = img_to_array(img)
print(imagen_en_array.shape)

archivo = open("../../Archivos/Unidad_2/p05_array_imagen_en_datos_c0.csv", "w")
for i in imagen_en_array:
    for j in i:
        archivo.write(str(j[canal]) + ",")
    archivo.write("\n")
archivo.flush()
archivo.close()
