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
        # Actualiza las barras de progreso
        temperatura_barra["value"] = temperature
        humedad_barra["value"] = humidity

        # Actualiza la posición de las barras de progreso verticales
        canvas.coords(temperatura_barra_vertical, 20, 200 - temperature, 60, 200)
        canvas.coords(humedad_barra_vertical, 100, 200 - humidity, 140, 200)

    root.after(1000, actualizar_barras)  # Actualiza cada segundo

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Sensor DHT11 - Barras de Temperatura y Humedad")

# Crear un lienzo (canvas) para las barras de progreso verticales
canvas = tk.Canvas(root, width=160, height=200)
canvas.pack()

# Crear barras de progreso verticales para temperatura y humedad
temperatura_barra = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
temperatura_barra["maximum"] = 40  # Puedes ajustar este valor según tus necesidades
temperatura_barra.pack(pady=10)
temperatura_label = ttk.Label(root, text="Temperatura (°C)")
temperatura_label.pack()

humedad_barra = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
humedad_barra["maximum"] = 100  # Puedes ajustar este valor según tus necesidades
humedad_barra.pack(pady=10)
humedad_label = ttk.Label(root, text="Humedad (%)")
humedad_label.pack()

# Barras de progreso verticales (en el lienzo)
temperatura_barra_vertical = canvas.create_rectangle(20, 0, 60, 0, fill="red")
humedad_barra_vertical = canvas.create_rectangle(100, 0, 140, 0, fill="blue")

# Iniciar la actualización de las barras
actualizar_barras()

# Iniciar la aplicación de Tkinter
root.mainloop()
