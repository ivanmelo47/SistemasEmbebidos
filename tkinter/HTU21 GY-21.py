import board
import busio
import adafruit_htu21d
import tkinter as tk
from tkinter import ttk

# Inicializa el bus I2C y el sensor HTU21D
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_htu21d.HTU21D(i2c)

# Función para leer los datos del sensor
def obtener_datos_sensor():
    temperature = sensor.temperature
    humidity = sensor.relative_humidity
    return humidity, temperature

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Sensor HTU21D - Temperatura y Humedad")

# Crear etiquetas para mostrar los valores de temperatura y humedad
temperatura_label = ttk.Label(root, text="", font=("Helvetica", 14))
temperatura_label.pack()
humedad_label = ttk.Label(root, text="", font=("Helvetica", 14))
humedad_label.pack()

# Función para actualizar los valores de temperatura y humedad
def actualizar_valores():
    humidity, temperature = obtener_datos_sensor()
    temperatura_label.config(text=f"Temperatura: {temperature:.2f}°C")
    humedad_label.config(text=f"Humedad: {humidity:.2f}%")
    root.after(1000, actualizar_valores)

# Iniciar la actualización de los valores
actualizar_valores()

# Iniciar la aplicación de Tkinter
root.mainloop()
