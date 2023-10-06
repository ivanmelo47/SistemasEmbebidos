import tkinter as tk
from RPi.GPIO import setmode, setup, output, BCM
import time

# Configuración de pines GPIO
setmode(BCM)
IN1 = 2  # Pin GPIO para IN1
IN2 = 3  # Pin GPIO para IN2
IN3 = 4  # Pin GPIO para IN3
IN4 = 17  # Pin GPIO para IN4

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

# Función para girar el motor en la dirección deseada
def girar_motor(pasos):
    for _ in range(pasos):
        for step in sequence:
            output(IN1, step[0])
            output(IN2, step[1])
            output(IN3, step[2])
            output(IN4, step[3])
            time.sleep(0.001)  # Ajusta la velocidad aquí

# Función para detener el motor
def detener_motor():
    output(IN1, LOW)
    output(IN2, LOW)
    output(IN3, LOW)
    output(IN4, LOW)

# Crear la ventana de la interfaz gráfica
root = tk.Tk()
root.title("Control de Motor Paso a Paso")

# Crear botones para controlar el motor
btn_horario = tk.Button(root, text="Sentido Horario")
btn_antihorario = tk.Button(root, text="Sentido Antihorario")
btn_detener = tk.Button(root, text="Detener")

# Configurar las funciones de los botones
def iniciar_sentido_horario(event):
    girar_motor(1)  # Girar un paso en sentido horario

def iniciar_sentido_antihorario(event):
    girar_motor(-1)  # Girar un paso en sentido antihorario

btn_horario.bind("<ButtonPress>", iniciar_sentido_horario)
btn_antihorario.bind("<ButtonPress>", iniciar_sentido_antihorario)
btn_detener.bind("<ButtonPress>", detener_motor)

# Colocar los botones en la ventana
btn_horario.pack()
btn_antihorario.pack()
btn_detener.pack()

# Iniciar la ventana principal
root.mainloop()
