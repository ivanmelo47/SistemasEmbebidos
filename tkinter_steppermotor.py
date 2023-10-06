import tkinter as tk
from RPi.GPIO import setmode, setup, output, BCM, OUT, HIGH, LOW
import time

# Configuración de pines GPIO
setmode(BCM)
IN1 = 2  # Pin GPIO para IN1
IN2 = 3  # Pin GPIO para IN2
IN3 = 4  # Pin GPIO para IN3
IN4 = 17  # Pin GPIO para IN4

setup(IN1, OUT)
setup(IN2, OUT)
setup(IN3, OUT)
setup(IN4, OUT)

# Función para girar el motor en sentido horario
def girar_sentido_horario():
    output(IN1, HIGH)
    output(IN2, LOW)
    output(IN3, LOW)
    output(IN4, LOW)

# Función para girar el motor en sentido antihorario
def girar_sentido_antihorario():
    output(IN1, LOW)
    output(IN2, LOW)
    output(IN3, LOW)
    output(IN4, HIGH)

# Función para detener el motor
def detener_motor():
    output(IN1, LOW)
    output(IN2, LOW)
    output(IN3, LOW)
    output(IN4, LOW)

# Función para iniciar el movimiento en sentido horario al presionar el botón
def iniciar_sentido_horario(event):
    girar_sentido_horario()

# Función para iniciar el movimiento en sentido antihorario al presionar el botón
def iniciar_sentido_antihorario(event):
    girar_sentido_antihorario()

# Función para detener el motor al soltar el botón
def detener(event):
    detener_motor()

# Crear la ventana de la interfaz gráfica
root = tk.Tk()
root.title("Control de Motor Paso a Paso")

# Crear botones para controlar el motor
btn_horario = tk.Button(root, text="Sentido Horario")
btn_antihorario = tk.Button(root, text="Sentido Antihorario")
btn_detener = tk.Button(root, text="Detener")

# Configurar las funciones de los botones
btn_horario.bind("<ButtonPress>", iniciar_sentido_horario)
btn_horario.bind("<ButtonRelease>", detener)
btn_antihorario.bind("<ButtonPress>", iniciar_sentido_antihorario)
btn_antihorario.bind("<ButtonRelease>", detener)
btn_detener.bind("<ButtonPress>", detener)

# Colocar los botones en la ventana
btn_horario.pack()
btn_antihorario.pack()
btn_detener.pack()

# Iniciar la ventana principal
root.mainloop()
