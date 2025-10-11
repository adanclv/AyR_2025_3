from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
import cv2
from keras.models import load_model
from keras.utils import load_img, img_to_array
import time

UMBRAL = 0.7

class CameraThread(QThread):
    Prediction = pyqtSignal(np.ndarray, tuple)

    def __init__(self, model_path, weights_path, width=300, height=300):
        super().__init__()
        self.running = True
        self.width = width
        self.height = height

        try:
            self.cnn = load_model(model_path)
            self.cnn.load_weights(weights_path)
        except Exception as e:
            print(f"Error al cargar el modelo/pesos: {e}")
            self.cnn = None

        self.face_classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def run(self):
        cam = cv2.VideoCapture(0)

        PREDICT_INTERVAL = 0.7  # s
        last_prediction_time = time.time()

        predict = (False, "✖️ Esperando primera predicción...")

        while self.running:
            ret, frame = cam.read()

            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if time.time() - last_prediction_time >= PREDICT_INTERVAL:
                last_prediction_time = time.time()
                predict = self.predict_face(frame)
            self.Prediction.emit(rgbImage, predict)

        cam.release()

    def stop(self):
        self.running = False
        self.wait()  # Espera a que el hilo termine

    def predict_face(self, image):
        # Detección de la cara en la imagen
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))

        if len(faces) > 0:
            (x, y, w, h) = faces[0]  # Tomamos la primera cara detectada
            face_frame = image[y:y + h, x:x + w]

            # Preprocesa la imagen de la cara
            face_frame = cv2.resize(face_frame, (self.height, self.width), interpolation=cv2.INTER_CUBIC)
            face_frame = cv2.cvtColor(face_frame, cv2.COLOR_BGR2GRAY)
            face_frame = img_to_array(face_frame)
            face_frame = face_frame / 255.0
            face_frame = np.expand_dims(face_frame, axis=0)

            # Realiza la predicción
            arreglo = self.cnn.predict(face_frame)

            probabilidad_maxima = np.max(arreglo[0])

            respuesta = np.argmax(arreglo[0])

            if probabilidad_maxima >= UMBRAL:
                resultado = "✅ Persona reconocida: "
                match respuesta:
                    case 0:
                        return (True ,resultado + "Adán")
                    case 1:
                        return (True, resultado + "Poncho")
                    case 2:
                        return (True, resultado + "Pavel")
                    case 3:
                        return (True, resultado + "Cristobal")
                    case _:
                        return (False, "✖️ Persona NO reconocida: idx inválido")
            else:
                return (False, "✖️ Persona NO reconocida: Desconocido")
        else: return (False, "✖️ No se detecta rostro")

