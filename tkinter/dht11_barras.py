import Adafruit_DHT
import tkinter as tk
from tkinter import ttk

# Configura el modelo del sensor y el número de pin GPIO
sensor = Adafruit_DHT.DHT11
pin = 4

# Función para obtener los datos del sensor
def obtener_datos_sensor():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return humidity, temperature

# Función para actualizar las barras de temperatura y humedad
def actualizar_barras():
    humidity, temperature = obtener_datos_sensor()
    if humidity is not None and temperature is not None:
        temperatura_barra["value"] = temperature
        humedad_barra["value"] = humidity
    root.after(1000, actualizar_barras)  # Actualiza cada segundo

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Sensor DHT11 - Barras de Temperatura y Humedad")

# Crear barras de progreso para temperatura y humedad
temperatura_barra = ttk.Progressbar(root, length=200, mode="determinate")
temperatura_barra["maximum"] = 40  # Puedes ajustar este valor según tus necesidades
temperatura_barra.pack(pady=10)
temperatura_label = ttk.Label(root, text="Temperatura (°C)")
temperatura_label.pack()

humedad_barra = ttk.Progressbar(root, length=200, mode="determinate")
humedad_barra["maximum"] = 100  # Puedes ajustar este valor según tus necesidades
humedad_barra.pack(pady=10)
humedad_label = ttk.Label(root, text="Humedad (%)")
humedad_label.pack()

# Iniciar la actualización de las barras
actualizar_barras()

# Iniciar la aplicación de Tkinter
root.mainloop()
