import Adafruit_DHT
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import time

# Configura el modelo del sensor y el número de pin GPIO
sensor = Adafruit_DHT.DHT11
pin = 4

# Función para obtener los datos del sensor
def obtener_datos_sensor():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return humidity, temperature

# Función para actualizar los gráficos
def actualizar_grafico(i):
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
        ax.relim()
        ax.autoscale_view()

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Sensor DHT11 - Gráfico de Temperatura y Humedad")

# Crear etiquetas para mostrar los valores de temperatura y humedad
temperatura_label = ttk.Label(root, text="", font=("Helvetica", 14))
temperatura_label.pack()
humedad_label = ttk.Label(root, text="", font=("Helvetica", 14))
humedad_label.pack()

# Crear una figura de Matplotlib
fig = Figure(figsize=(6, 4), dpi=100)
ax = fig.add_subplot(111)
xdata, ydata_temp, ydata_hum = [], [], []
line_temp, = ax.plot(xdata, ydata_temp, 'r', label="Temperatura (°C)")
line_hum, = ax.plot(xdata, ydata_hum, 'g', label="Humedad (%)")
ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Valor")
ax.set_title("Temperatura y Humedad en Tiempo Real")
ax.legend()

# Crear el lienzo de Matplotlib
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Actualizar los gráficos cada segundo
ani = animation.FuncAnimation(fig, actualizar_grafico, interval=1000)

# Iniciar la aplicación de Tkinter
root.mainloop()
