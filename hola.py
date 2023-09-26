import tkinter as tk
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

# Función para obtener la temperatura del procesador
def get_cpu_temp():
    try:
        temp = psutil.sensors_temperatures()['coretemp'][0].current
        return temp
    except Exception as e:
        print("Error al obtener la temperatura:", e)
        return None

# Función para actualizar el gráfico de temperatura
def update_plot():
    temp = get_cpu_temp()
    if temp is not None:
        temp_values.append(temp)
        temp_labels.append(time.strftime("%H:%M:%S"))
        if len(temp_values) > 10:
            temp_values.pop(0)
            temp_labels.pop(0)
        ax.clear()
        ax.plot(temp_labels, temp_values, marker='o', linestyle='-')
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Temperatura (°C)')
        ax.set_title('Temperatura del Procesador')
        canvas.draw()
    root.after(1000, update_plot)

# Crear la ventana de la aplicación
root = tk.Tk()
root.title("Monitor de Temperatura del Procesador")

# Crear un gráfico para mostrar la temperatura
fig, ax = plt.subplots()
temp_values = []
temp_labels = []

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Botón para salir de la aplicación
exit_button = tk.Button(root, text="Salir", command=root.quit)
exit_button.pack()

# Iniciar la actualización del gráfico
update_plot()

# Iniciar la aplicación
root.mainloop()
