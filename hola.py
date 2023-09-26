import tkinter as tk
from smbus2 import SMBus
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Dirección I2C del sensor GY-21 (puede variar)
address = 0x40

# Inicializar el bus I2C
bus = SMBus(1)

# Listas para almacenar datos de temperatura y tiempo
temperature_data = []
time_data = []

# Función para leer datos de temperatura
def read_temperature():
    data = bus.read_i2c_block_data(address, 0xE5, 2)
    raw_temp = (data[0] << 8) + data[1]
    temperature = ((175.72 * raw_temp) / 65536.0) - 46.85
    return temperature

# Función para actualizar la temperatura y la gráfica
def update_temperature():
    temp = read_temperature()
    temperature_data.append(temp)
    time_data.append(len(temperature_data))

    # Actualizar la etiqueta de temperatura
    temperature_label.config(text=f"Temperatura: {temp}°C")

    # Actualizar la gráfica
    ax.clear()
    ax.plot(time_data, temperature_data, marker='o', linestyle='-')
    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Temperatura (°C)')
    canvas.draw()

    root.after(2000, update_temperature)  # Actualizar cada 2 segundos

# Crear la ventana principal
root = tk.Tk()
root.title("Sensor GY-21")

# Etiqueta para mostrar la temperatura
temperature_label = tk.Label(root, text="", font=("Arial", 24))
temperature_label.pack(padx=20, pady=20)

# Configurar la gráfica
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
ax.set_xlabel('Tiempo')
ax.set_ylabel('Temperatura (°C)')

# Iniciar la actualización de temperatura y la gráfica
update_temperature()

# Ejecutar la aplicación
root.mainloop()
