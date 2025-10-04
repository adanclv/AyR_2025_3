import cv2
import mediapipe as mp
import time

interval = 3 # s

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Configuración: detectar máx 2 manos, con confianza mínima
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
hand_landmarks_dic = {
    "thumb": (4, 3),
    "index": (8, 5),
    "middle": (12, 9),
    "ring": (16, 13),
    "pinky": (20, 17),
}
h, w = 480, 640

# Captura de cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (w, h))

    if not ret:
        break

    # Convertir BGR -> RGB (MediaPipe usa RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    # Dibujar landmarks si se detectan manos
    if result.multi_hand_landmarks:
        fingers_up = 0
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            for key, (lm1, lm2) in hand_landmarks_dic.items():
                if key == "thumb":
                    is_up = hand_landmarks.landmark[lm1].x < hand_landmarks.landmark[lm2].x
                else:
                    is_up = hand_landmarks.landmark[lm1].y < hand_landmarks.landmark[lm2].y

                if is_up:
                    fingers_up += 1
                    cx, cy = int(hand_landmarks.landmark[lm1].x * w), int(hand_landmarks.landmark[lm1].y * h)
                    cv2.circle(frame, (cx, cy), 15, (0, 255, 0), -1)

        cv2.putText(frame, f"Dedos levantados: {fingers_up}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Camara", frame)

    res = cv2.waitKey(1)
    if res == ord("q"):  # q para salir
        break

cap.release()
cv2.destroyAllWindows()
