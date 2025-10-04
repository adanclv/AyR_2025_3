import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def contar_dedos(hand_landmarks, handedness):
    dedos = []

    # Pulgar
    if handedness == "Right":
        if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
            dedos.append(1)
        else:
            dedos.append(0)
    else:  # Left
        if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
            dedos.append(1)
        else:
            dedos.append(0)

    # Índice, medio, anular, meñique (compara eje Y)
    for tip in [8, 12, 16, 20]:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            dedos.append(1)
        else:
            dedos.append(0)

    return sum(dedos)

cap = cv2.VideoCapture(0)

with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.75) as manos:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = manos.process(rgb)

        if results.multi_hand_landmarks:
            numeros = []
            for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks,
                                                       results.multi_handedness):
                # Saber si es mano izquierda o derecha
                label = hand_handedness.classification[0].label  # "Left" o "Right"

                # Contar dedos con función que recibe también el label
                dedos = contar_dedos(hand_landmarks, label)
                numeros.append(dedos)

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Si detecta dos manos → suma
            if len(numeros) == 2:
                suma = numeros[0] + numeros[1]
                cv2.putText(frame, f"{numeros[0]} + {numeros[1]} = {suma}",
                            (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            # Si detecta una mano → solo muestra número
            elif len(numeros) == 1:
                cv2.putText(frame, f"Numero: {numeros[0]}",
                            (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

        cv2.imshow("Suma con manos", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC para salir
            break

cap.release()
cv2.destroyAllWindows()