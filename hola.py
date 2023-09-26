import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import psutil

# Función para obtener la temperatura del procesador en grados Celsius
def get_cpu_temperature():
    try:
        temp = psutil.sensors_temperatures()['coretemp'][0].current
        return temp
    except (KeyError, FileNotFoundError, AttributeError):
        return None

# Función para actualizar el gráfico
def actualizar_grafico():
    temperatura = get_cpu_temperature()
    if temperatura is not None:
        etiqueta_temperatura.config(text=f"Temperatura del procesador: {temperatura} °C")
        historial_temperatura.append(temperatura)
        ax.clear()
        ax.plot(historial_temperatura, marker='o', linestyle='-')
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Temperatura (°C)')
        canvas.draw()
    ventana.after(1000, actualizar_grafico)  # Actualiza cada 1 segundo

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Monitor de Temperatura del Procesador")

# Crear una etiqueta para mostrar la temperatura actual
etiqueta_temperatura = tk.Label(ventana, text="", font=("Helvetica", 16))
etiqueta_temperatura.pack(pady=10)

# Crear un gráfico para mostrar el historial de temperaturas
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

historial_temperatura = []

# Iniciar la actualización del gráfico
actualizar_grafico()

# Iniciar el bucle principal
ventana.mainloop()
