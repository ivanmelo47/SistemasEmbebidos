import smbus2
import time
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Configura los pines GPIO
# (Asumiendo que utilizas los pines GPIO 27 y GPIO 22)
SDA_PIN = 27
SCL_PIN = 22

# Dirección I2C del sensor GY-21
address = 0x40

# Inicializar el bus I2C
bus = smbus2.SMBus(1)

# Función para leer datos de temperatura y humedad
def read_sensor_data():
    data = bus.read_i2c_block_data(address, 0xE5, 2)
    raw_temp = (data[0] << 8) + data[1]
    temperature = ((175.72 * raw_temp) / 65536.0) - 46.85
    return temperature

# Función para actualizar los valores de temperatura y humedad
def update_values():
    temp = read_sensor_data()
    humidity_label.config(text=f"Temperatura: {temp:.2f}°C")
    humidity = 0  # Reemplaza con la lectura real de la humedad
    humidity_label.config(text=f"Humedad: {humidity:.2f}%")
    update_graph(temp, humidity)
    root.after(2000, update_values)  # Actualiza cada 2 segundos

# Función para actualizar el gráfico
def update_graph(temp, humidity):
    temp_data.append(temp)
    humidity_data.append(humidity)
    if len(temp_data) > 10:
        temp_data.pop(0)
        humidity_data.pop(0)
    ax.clear()
    ax.plot(range(len(temp_data)), temp_data, label='Temperatura')
    ax.plot(range(len(humidity_data)), humidity_data, label='Humedad')
    ax.set_xlabel('Muestras')
    ax.set_ylabel('Valor')
    ax.set_title('Temperatura y Humedad')
    ax.legend()

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Sensor GY-21")

# Etiquetas para mostrar la temperatura y la humedad
temperature_label = tk.Label(root, text="Temperatura: ", font=("Helvetica", 14))
temperature_label.pack()
humidity_label = tk.Label(root, text="Humedad: ", font=("Helvetica", 14))
humidity_label.pack()

# Configurar el gráfico
fig = Figure(figsize=(6, 4), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Inicializar listas de datos para el gráfico
temp_data = []
humidity_data = []

# Iniciar la actualización de valores y gráfico
update_values()

# Ejecutar la aplicación Tkinter
root.mainloop()
