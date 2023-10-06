import RPi.GPIO as GPIO
import time

# Define los pines GPIO que están conectados a IN1, IN2, IN3, IN4
IN1 = 2
IN2 = 3
IN3 = 4
IN4 = 17

# Configura los pines GPIO como salida
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Secuencia de pasos para girar el motor en sentido horario
sequence = [
    (1, 0, 0, 0),
    (1, 1, 0, 0),
    (0, 1, 0, 0),
    (0, 1, 1, 0),
    (0, 0, 1, 0),
    (0, 0, 1, 1),
    (0, 0, 0, 1),
    (1, 0, 0, 1),
]

# Calcula el número de pasos para una vuelta completa (360 grados)
pasos_por_vuelta = 4096  # Esto es para el motor 28BYJ-48

# Define la velocidad (ajusta este valor para cambiar la velocidad)
velocidad_s = 0.001  # Tiempo de espera en segundos entre pasos (mayor valor = menor velocidad)

# Gira el motor en sentido horario para una vuelta completa
for _ in range(pasos_por_vuelta):
    for step in sequence:
        GPIO.output(IN1, step[0])
        GPIO.output(IN2, step[1])
        GPIO.output(IN3, step[2])
        GPIO.output(IN4, step[3])
        time.sleep(velocidad_s)  # Ajusta la velocidad aquí

# Detiene el motor
GPIO.cleanup()
