import tkinter as tk
import RPi.GPIO as GPIO
import time

# Configura los pines GPIO
IN1 = 2  # Pin IN1 de la placa ULN2003A (ajusta según tu configuración)
IN2 = 3  # Pin IN2 de la placa ULN2003A (ajusta según tu configuración)
IN3 = 4  # Pin IN3 de la placa ULN2003A (ajusta según tu configuración)
IN4 = 17  # Pin IN4 de la placa ULN2003A (ajusta según tu configuración)

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

#Secuencia de pasos para girar el motor en sentido horario
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

#Secuencia en reversa
sequence_ccw = list(reversed(sequence))

# Grados que dara vuelta el motor
grados = 360

# Calcula el número de pasos para una vuelta completa (360 grados)
pasos_por_vuelta = ((grados * 510)/360)  # Esto es para el motor 28BYJ-48

# Define la velocidad (ajusta este valor para cambiar la velocidad)
velocidad_s = 0.001  # Tiempo de espera en segundos entre pasos (mayor valor = menor velocidad)

# Crea una ventana de Tkinter
window = tk.Tk()
window.title("Control de Motor Paso a Paso")

# Función para mover el motor en sentido horario
def move_clockwise():
    # Gira el motor en sentido horario para una vuelta completa
    for _ in range(pasos_por_vuelta):
        for step in sequence:
            GPIO.output(IN1, step[0])
            GPIO.output(IN2, step[1])
            GPIO.output(IN3, step[2])
            GPIO.output(IN4, step[3])
            time.sleep(velocidad_s)  # Ajusta la velocidad aquí

# Función para mover el motor en sentido antihorario
def move_counterclockwise():
    for _ in range(pasos_por_vuelta):
        for step in sequence_ccw:
            GPIO.output(IN1, step[0])
            GPIO.output(IN2, step[1])
            GPIO.output(IN3, step[2])
            GPIO.output(IN4, step[3])
            time.sleep(velocidad_s)  # Ajusta la velocidad aquí

# Función para detener el motor
def stop_motor():
    # Detiene el motor
    GPIO.cleanup()

# Crea los botones para controlar el motor
clockwise_button = tk.Button(window, text="Sentido Horario", command=move_clockwise)
clockwise_button.pack()

counterclockwise_button = tk.Button(window, text="Sentido Antihorario", command=move_counterclockwise)
counterclockwise_button.pack()

stop_button = tk.Button(window, text="Detener", command=stop_motor)
stop_button.pack()

# Función para detener el motor al cerrar la ventana
def on_closing():
    stop_motor()
    GPIO.cleanup()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()
