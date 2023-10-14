import RPi.GPIO as GPIO
import Adafruit_DHT
import asyncio
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import numpy as np

# Configura los pines GPIO y otros valores
pin_base = 19  # Debes asignar el pin GPIO correcto de la Raspberry Pi

# Define el modelo del sensor y el número de pin GPIO
sensor = Adafruit_DHT.DHT11
pin_dht = 4  # Debes asignar el pin GPIO correcto de la Raspberry Pi

# Define los pines GPIO que están conectados a IN1, IN2, IN3, IN4
IN1 = 17
IN2 = 27
IN3 = 22
IN4 = 10

sequence_cw = [
    (1, 0, 0, 0),
    (1, 1, 0, 0),
    (0, 1, 0, 0),
    (0, 1, 1, 0),
    (0, 0, 1, 0),
    (0, 0, 1, 1),
    (0, 0, 0, 1),
    (1, 0, 0, 1),
]

sequence_ccw = list(reversed(sequence_cw))

pasos_por_vuelta = 510
velocidad_ms = 0.001
vuelta = True

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_base, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Variables para controlar la adquisición de datos
adquirir_datos = False

# Función para obtener los datos del sensor
def obtener_datos_sensor():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin_dht)
    return humidity, temperature

# Función para mover el motor de paso
def mover_motor():
    global vuelta
    if not vuelta:
        return
    for _ in range(pasos_por_vuelta):
        for step in sequence_cw:
            GPIO.output(IN1, step[0])
            GPIO.output(IN2, step[1])
            GPIO.output(IN3, step[2])
            GPIO.output(IN4, step[3])
            time.sleep(velocidad_ms)
    GPIO.output(pin_base, GPIO.HIGH)
    vuelta = False

# Función para actualizar los gráficos
def actualizar_grafico(i):
    if adquirir_datos:
        humidity, temperature = obtener_datos_sensor()
        if humidity is not None and temperature is not None:
            if temperature > 26:  # Agrega la condición para mover el motor
                mover_motor()
            xdata_temp.append(time.time())
            ydata_temp.append(temperature)
            xdata_hum.append(time.time())
            ydata_hum.append(humidity)
            if len(xdata_temp) > 20:
                xdata_temp.pop(0)
                ydata_temp.pop(0)
                xdata_hum.pop(0)
                ydata_hum.pop(0)
            line_temp.set_data(xdata_temp, ydata_temp)
            line_hum.set_data(xdata_hum, ydata_hum)
            ax_temp.relim()
            ax_temp.autoscale_view()
            ax_hum.relim()
            ax_hum.autoscale_view()
            temperatura_label.config(text=f"Temperatura: {temperature:.2f}°C")
            humedad_label.config(text=f"Humedad: {humidity:.2f}%")

# Función para iniciar la adquisición de datos
def iniciar_adquisicion():
    global adquirir_datos
    adquirir_datos = True

# Función para detener la adquisición de datos
def detener_adquisicion():
    global adquirir_datos
    adquirir_datos = False

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Sensor DHT11 - Gráficos de Temperatura y Humedad")

# Crear un marco (frame) para los gráficos de temperatura
frame_temp = ttk.Frame(root)
frame_temp.pack(side=tk.LEFT, padx=10, pady=10)
frame_temp.grid(column=0, row=0)
frame_temp.grid_propagate(0)  # Evita que el marco cambie de tamaño automáticamente

# Crear un marco (frame) para los gráficos de humedad
frame_hum = ttk.Frame(root)
frame_hum.pack(side=tk.LEFT, padx=10, pady=10)
frame_hum.grid(column=1, row=0)
frame_hum.grid_propagate(0)  # Evita que el marco cambie de tamaño automáticamente

# Crear etiquetas para mostrar los valores de temperatura y humedad
temperatura_label = ttk.Label(frame_temp, text="", font=("Helvetica", 14))
temperatura_label.pack()
humedad_label = ttk.Label(frame_hum, text="", font=("Helvetica", 14))
humedad_label.pack()

# Crear botones para iniciar y detener la adquisición de datos
iniciar_button = ttk.Button(root, text="Iniciar", command=iniciar_adquisicion)
iniciar_button.pack()
detener_button = ttk.Button(root, text="Detener", command=detener_adquisicion)
detener_button.pack()

# Crear una figura de Matplotlib con dos subgráficos en el marco de temperatura
fig_temp = Figure(figsize=(6, 4), dpi=100)
ax_temp = fig_temp.add_subplot(111)
xdata_temp, ydata_temp = [], []
line_temp
