import Adafruit_DHT
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import time

import RPi.GPIO as GPIO
import asyncio

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

# Funcion para controlar el motor
async def control_motor():
    global vuelta
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin_dht)
        
        if humidity is not None and temperature is not None:
            if vuelta and temperature >= 26:
                for _ in range(pasos_por_vuelta):
                    for step in sequence_cw:
                        GPIO.output(IN1, step[0])
                        GPIO.output(IN2, step[1])
                        GPIO.output(IN3, step[2])
                        GPIO.output(IN4, step[3])
                        time.sleep(velocidad_ms)
                GPIO.output(pin_base, GPIO.HIGH)
                vuelta = False
            elif not vuelta and temperature < 26:
                for _ in range(pasos_por_vuelta):
                    for step in sequence_ccw:
                        GPIO.output(IN1, step[0])
                        GPIO.output(IN2, step[1])
                        GPIO.output(IN3, step[2])
                        GPIO.output(IN4, step[3])
                        time.sleep(velocidad_ms)
                GPIO.output(pin_base, GPIO.LOW)
                vuelta = True
        await asyncio.sleep(1)

# Función para obtener los datos del sensor
def obtener_datos_sensor():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin_dht)
    return humidity, temperature

# Función para actualizar los gráficos
def actualizar_grafico(i):
    global adquirir_datos
    if adquirir_datos:
        humidity, temperature = obtener_datos_sensor()
        if humidity is not None and temperature is not None:
            temperatura_label.config(text=f"Temperatura: {temperature:.2f}°C")
            humedad_label.config(text=f"Humedad: {humidity:.2f}%")
            xdata.append(time.time())
            ydata_temp.append(temperature)
            ydata_hum.append(humidity)
            if len(xdata) > 20:
                xdata.pop(0)
                ydata_temp.pop(0)
                ydata_hum.pop(0)
            line_temp.set_data(xdata, ydata_temp)
            line_hum.set_data(xdata, ydata_hum)
            ax_temp.relim()
            ax_temp.autoscale_view()
            ax_hum.relim()
            ax_hum.autoscale_view()

# Función para iniciar la adquisición de datos
def iniciar_adquisicion():
    global adquirir_datos
    adquirir_datos = True
    control_motor()

# Función para detener la adquisición de datos
def detener_adquisicion():
    global adquirir_datos
    adquirir_datos = False

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Sensor DHT11 - Gráficos de Temperatura y Humedad")

# Crear etiquetas para mostrar los valores de temperatura y humedad
temperatura_label = ttk.Label(root, text="", font=("Helvetica", 14))
temperatura_label.pack()
humedad_label = ttk.Label(root, text="", font=("Helvetica", 14))
humedad_label.pack()

# Crear botones para iniciar y detener la adquisición de datos
iniciar_button = ttk.Button(root, text="Iniciar", command=iniciar_adquisicion)
iniciar_button.pack()
detener_button = ttk.Button(root, text="Detener", command=detener_adquisicion)
detener_button.pack()

# Crear una figura de Matplotlib con dos subgráficos
fig = Figure(figsize=(8, 6), dpi=100)
ax_temp = fig.add_subplot(211)
ax_hum = fig.add_subplot(212)
xdata, ydata_temp, ydata_hum = [], [], []
line_temp, = ax_temp.plot(xdata, ydata_temp, 'r', label="Temperatura (°C)")
line_hum, = ax_hum.plot(xdata, ydata_hum, 'g', label="Humedad (%)")
ax_temp.set_ylabel("Temperatura (°C)")
ax_hum.set_ylabel("Humedad (%)")
ax_hum.set_xlabel("Tiempo (s)")
ax_temp.set_title("Gráfico de Temperatura")
ax_hum.set_title("Gráfico de Humedad")
ax_temp.legend()
ax_hum.legend()

# Crear el lienzo de Matplotlib
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Actualizar los gráficos cada segundo
ani = animation.FuncAnimation(fig, actualizar_grafico, interval=1000)

# Iniciar la aplicación de Tkinter
root.mainloop()
