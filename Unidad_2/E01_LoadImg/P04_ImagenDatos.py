from keras.utils import load_img, img_to_array

largo, alto = 300, 200

file = "../../Archivos/Images/airplane1.jpeg"

img = load_img(file, target_size = (largo, alto)
               #, color_mode ="grayscale"
               )

print(img.size)
print(img.mode)

imagen_en_array = img_to_array(img)
print(imagen_en_array.shape)

archivo = open("../../Archivos/Unidad_2/p04_array_imagen_en_datos.csv", "w")
for i in imagen_en_array:
    for j in i:
        archivo.write(str(j[0])+ " , ")
    archivo.write("\n")
archivo.flush()
archivo.close()
