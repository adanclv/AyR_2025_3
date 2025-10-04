from PyQt5 import uic, QtWidgets, QtGui, QtCore
import sys
import cv2
import mediapipe as mp

qtCreatorFile = "Ui_Gestos.ui"  # Nombre del archivo UI
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Inicializar Mediapipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

        # Cámara y timer
        self.camera = None
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Botón
        self.btn_start.clicked.connect(self.toggle_camera)

        self.is_running = False

    def update_frame(self):
        if not self.camera:
            return

        ret, frame = self.camera.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        # Convertir a RGB para Mediapipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        # Dibujar landmarks si hay manos detectadas
        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                # Detectar dedos
                estado = detectar_dedos(hand_landmarks, handedness.classification[0].label)
                mensaje = []
                pulgar, indice, menique = estado.values()
                if all([pulgar, indice, menique]):
                    mensaje.append("Stop")
                else:
                    if pulgar: mensaje.append("Avanzar")
                    if indice: mensaje.append("Izquierda")
                    if menique: mensaje.append("Derecha")

                if mensaje:
                    self.txt_gesto.setText(" + ".join(mensaje) if len(mensaje) > 1 else mensaje[0])
                else:
                    self.txt_gesto.setText("Ningún dedo levantado")

        # Convertir a QImage para mostrar en QLabel
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        q_img = QtGui.QImage(rgb_frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)

        pixmap = QtGui.QPixmap.fromImage(q_img)
        self.lbl_video.setPixmap(pixmap.scaled(self.lbl_video.size(), QtCore.Qt.KeepAspectRatio))

    def closeEvent(self, event):
        if self.camera:
            self.camera.release()
        event.accept()

    def toggle_camera(self):
        if not self.is_running:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                self.txt_gesto.setText("No se pudo abrir la cámara")
                return
            self.timer.start(50)
            self.btn_start.setText("Detener Cámara")
            self.is_running = True
        else:
            self.timer.stop()
            if self.camera:
                self.camera.release()
                self.camera = None
            self.btn_start.setText("Iniciar Cámara")
            # self.txt_gesto.setText("Predicción: N/A")
            self.lbl_video.clear()
            self.is_running = False

def detectar_dedos(hand_landmarks, handedness="Right"):
    lm = hand_landmarks.landmark
    dedos = {
        "pulgar": False,
        "indice": False,
        "menique": False
    }

    if handedness == "Right":
        if lm[4].x < lm[3].x:
            dedos["pulgar"] = True
    else:
        if lm[4].x > lm[3].x:
            dedos["pulgar"] = True

    if lm[8].y < lm[6].y:
        dedos["indice"] = True

    if lm[20].y < lm[18].y:
        dedos["menique"] = True

    return dedos


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
