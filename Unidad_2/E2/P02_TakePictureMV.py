import cv2  ##opencv
import time
cam = cv2.VideoCapture(0) ##videocamara --- Si ocupas OBS pon 1
_start_time = time.time()

path = "../../Archivos/Images/"
name = "john"
default_name = path + name + "_foto_"
contFotos = 0
totalFotos = 500

interval = 5000  # ms
previous_millis = 0

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def face_detect_box(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    faces_frames = []
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 4)

        aux = image.copy()
        faces_frames.append(aux[y:y+h, x:x+w])

    return faces, faces_frames

def milliseconds():
    return int((time.time() - _start_time) * 1000)

while True:
    result, image = cam.read()
    current_millis = milliseconds()

    if result:
        faces_detected, img_faces = face_detect_box(image)
        cv2.imshow("CamaraV_OBS", image)
        res = cv2.waitKey(1) ## 1  = .. De esta manera la ejecucion continua
        # aunque el usuario no presione alguna tecla

        if res == ord("q") or contFotos >= totalFotos:
            cam.release()
            cv2.destroyWindow("CamaraV_OBS")
            break

        if current_millis - previous_millis >= interval:
            previous_millis = current_millis
            if len(img_faces) == 0:
                cv2.imwrite(default_name + "full_" + str(contFotos) + ".png", image)
                # contFotos += 1
            else:
                for img in img_faces:
                    imagen_cara = cv2.resize(img, (400, 400), interpolation=cv2.INTER_CUBIC)
                    cv2.imwrite(default_name + str(contFotos) + ".png", imagen_cara)
                    contFotos += 1
            print("Foto No." + str(contFotos))
    else:
        print("No image detected. Please! try again")
        break


