import sys
import os
from PyQt5 import uic, QtWidgets, QtGui, QtCore
import cv2
import numpy as np
from keras.models import load_model
from keras.utils import load_img, img_to_array
import time
qtCreatorFile = "Interfaz_Verificacion.ui"  # Nombre del archivo aquí.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# Carga la CNN una sola vez al inicio
alto, largo = 300, 300
modelo = "../E04_CNN/modelo/modelo.keras"
pesos = '../E04_CNN/modelo/pesos.weights.h5'
cnn = load_model(modelo)
cnn.load_weights(pesos)

# Define el clasificador de caras
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def predict_face(image):
    # Detección de la cara en la imagen
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))

    if len(faces) > 0:
        (x, y, w, h) = faces[0]  # Tomamos la primera cara detectada
        face_frame = image[y:y + h, x:x + w]

        # Preprocesa la imagen de la cara
        face_frame = cv2.resize(face_frame, (alto, largo), interpolation=cv2.INTER_CUBIC)
        face_frame = cv2.cvtColor(face_frame, cv2.COLOR_BGR2GRAY)
        face_frame = img_to_array(face_frame)
        face_frame = face_frame / 255.0
        face_frame = np.expand_dims(face_frame, axis=0)

        # Realiza la predicción
        arreglo = cnn.predict(face_frame)
        respuesta = np.argmax(arreglo[0])

        # Devuelve el resultado
        match respuesta:
            case 0:
                return 'C1-Adan'
            case 1:
                return 'C2-Poncho'
            case 2:
                return 'C3-Pavel'
            case 3:
                return 'C4-Cristobal'
            case _:
                return '----'

    return "No hay cara"
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Área de los Signals
        # Configura la cámara y el temporizador
        self.camera = cv2.VideoCapture(0)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Conecta los botones
        self.startButton.clicked.connect(self.toggle_camera)

        self.is_running = False
    # Área de los Slots
    def toggle_camera(self):
        if not self.is_running:
            self.timer.start(50)  # Actualiza cada 50ms
            self.startButton.setText("Detener Cámara")
            self.is_running = True
        else:
            self.timer.stop()
            self.startButton.setText("Iniciar Cámara")
            self.predictionLabel.setText("Predicción: N/A")
            self.videoLabel.clear()
            self.is_running = False

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.flip(frame, 1)  # Voltea el video horizontalmente

            # Convierte el frame de OpenCV a QPixmap para mostrarlo
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(convertToQtFormat)
            self.videoLabel.setPixmap(pixmap.scaled(self.videoLabel.size(), QtCore.Qt.KeepAspectRatio))

            # Realiza la predicción y actualiza la etiqueta
            prediction = predict_face(frame)
            self.predictionLabel.setText(f"Predicción: {prediction}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())