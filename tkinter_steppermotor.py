import tkinter as tk
import RPi.GPIO as GPIO
import time

# Configura los pines GPIO
IN1 = 2  # Pin GPIO para IN1
IN2 = 3  # Pin GPIO para IN2
IN3 = 4  # Pin GPIO para IN3
IN4 = 17  # Pin GPIO para IN4

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Funciones para controlar el motor
def girar_sentido_horario():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def girar_sentido_antihorario():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def detener_motor():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

# Crear la ventana de la interfaz gráfica
root = tk.Tk()
root.title("Control de Motor Paso a Paso")

# Funciones para controlar el motor cuando se mantienen presionados los botones
def comenzar_giro_horario(event):
    girar_sentido_horario()

def comenzar_giro_antihorario(event):
    girar_sentido_antihorario()

def detener_giro(event):
    detener_motor()

# Crear botones para controlar el motor
btn_horario = tk.Button(root, text="Girar Horario")
btn_antihorario = tk.Button(root, text="Girar Antihorario")
btn_detener = tk.Button(root, text="Detener")

# Configurar las funciones de control de motor para eventos de clic
btn_horario.bind("<ButtonPress>", comenzar_giro_horario)
btn_horario.bind("<ButtonRelease>", detener_giro)
btn_antihorario.bind("<ButtonPress>", comenzar_giro_antihorario)
btn_antihorario.bind("<ButtonRelease>", detener_giro)
btn_detener.bind("<ButtonPress>", detener_giro)

# Colocar los botones en la ventana
btn_horario.pack()
btn_antihorario.pack()
btn_detener.pack()

# Iniciar la ventana principal
root.mainloop()
