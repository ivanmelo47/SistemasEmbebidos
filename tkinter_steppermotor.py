import tkinter as tk
import RPi.GPIO as GPIO
import time

# Configura los pines GPIO
IN1 = 2  # Pin IN1 de la placa ULN2003A (ajusta según tu configuración)
IN2 = 3  # Pin IN2 de la placa ULN2003A (ajusta según tu configuración)
IN3 = 4  # Pin IN3 de la placa ULN2003A (ajusta según tu configuración)
IN4 = 5  # Pin IN4 de la placa ULN2003A (ajusta según tu configuración)

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Crea una ventana de Tkinter
window = tk.Tk()
window.title("Control de Motor Paso a Paso")

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

# Función para mover el motor en sentido horario
def move_clockwise():
    for step in sequence:
        GPIO.output(IN1, step[0])
        GPIO.output(IN2, step[1])
        GPIO.output(IN3, step[2])
        GPIO.output(IN4, step[3])
        time.sleep(0.001)  # Ajusta la velocidad aquí

# Función para mover el motor en sentido antihorario (detenido en este caso)
def move_counterclockwise():
    stop_motor()

# Función para detener el motor
def stop_motor():
    GPIO.output(IN1, 0)
    GPIO.output(IN2, 0)
    GPIO.output(IN3, 0)
    GPIO.output(IN4, 0)

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
