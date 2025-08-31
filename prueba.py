import time
_start_time = time.time()

def millis():
    return int((time.time() - _start_time) * 1000)

interval = 1000  # ms
previousMillis = 0

while True:
    currentMillis = millis()
    if currentMillis - previousMillis >= interval:
        print(currentMillis, " - ", previousMillis)
        previousMillis = currentMillis