import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import asyncio
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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

# Configuración de los pines GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_base, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Listas para almacenar datos de temperatura y humedad
temperature_data = []
humidity_data = []
time_data = []

# Funciones para actualizar las gráficas de temperatura y humedad
def update_temperature_plot():
    temperature_canvas.draw()

def update_humidity_plot():
    humidity_canvas.draw()

# Función para actualizar las gráficas
def update_plots():
    update_temperature_plot()
    update_humidity_plot()

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
                        await asyncio.sleep(velocidad_ms)
                GPIO.output(pin_base, GPIO.HIGH)
                vuelta = False
            elif not vuelta and temperature < 26:
                for _ in range(pasos_por_vuelta):
                    for step in sequence_ccw:
                        GPIO.output(IN1, step[0])
                        GPIO.output(IN2, step[1])
                        GPIO.output(IN3, step[2])
                        GPIO.output(IN4, step[3])
                        await asyncio.sleep(velocidad_ms)
                GPIO.output(pin_base, GPIO.LOW)
                vuelta = True
        await asyncio.sleep(1)

async def lectura_sensor():
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin_dht)
        if humidity is not None and temperature is not None:
            print(f"\rTemperatura: {temperature:.2f}°C, Humedad: {humidity:.2f}%", end="")
            # Guardar los datos en las listas
            temperature_data.append(temperature)
            humidity_data.append(humidity)
            time_data.append(time.time())
            # Actualizar las gráficas
            update_plots()
        await asyncio.sleep(1)

async def main():
    await asyncio.gather(control_motor(), lectura_sensor())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    root = tk.Tk()
    root.title("Temperatura y Humedad")

    # Crear una figura para la temperatura
    temperature_fig = Figure(figsize=(5, 3), dpi=100)
    temperature_canvas = FigureCanvasTkAgg(temperature_fig, master=root)
    temperature_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Crear una figura para la humedad
    humidity_fig = Figure(figsize=(5, 3), dpi=100)
    humidity_canvas = FigureCanvasTkAgg(humidity_fig, master=root)
    humidity_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    plt.ion()  # Habilita el modo interactivo de matplotlib

    loop.run_until_complete(main())
    root.mainloop()
