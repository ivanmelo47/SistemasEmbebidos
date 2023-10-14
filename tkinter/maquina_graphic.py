import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import asyncio
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation

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

motor_encendido = False

async def control_motor():
    global vuelta, motor_encendido
    while True:
        if motor_encendido:
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

async def lectura_sensor():
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin_dht)
        if humidity is not None and temperature is not None:
            print(f"\rTemperatura: {temperature:.2f}°C, Humedad: {humidity:.2f}%", end="")
        await asyncio.sleep(1)

def cambiar_estado_motor():
    global motor_encendido
    motor_encendido = not motor_encendido

xdata, ydata_temp, ydata_hum = []

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Sensor DHT11 - Gráficos de Temperatura y Humedad")

# Crear etiquetas para mostrar los valores de temperatura y humedad
temperatura_label = ttk.Label(root, text="", font=("Helvetica", 14))
temperatura_label.pack()
humedad_label = ttk.Label(root, text="", font=("Helvetica", 14))
humedad_label.pack()

# Crear botones para iniciar y detener el motor y la adquisición de datos
motor_button = ttk.Button(root, text="Iniciar/Detener Motor", command=cambiar_estado_motor)
motor_button.pack()

# Crear una figura de Matplotlib con dos subgráficos
fig_temp = Figure(figsize=(8, 4), dpi=100)
ax_temp = fig_temp.add_subplot(211)
ax_temp.set_ylabel("Temperatura (°C)")
ax_temp.set_title("Gráfico de Temperatura")
line_temp, = ax_temp.plot(xdata, ydata_temp, 'r-')

fig_hum = Figure(figsize=(8, 4), dpi=100)
ax_hum = fig_hum.add_subplot(212)
ax_hum.set_xlabel("Tiempo (s)")
ax_hum.set_ylabel("Humedad (%)")
ax_hum.set_title("Gráfico de Humedad")
line_hum, = ax_hum.plot(xdata, ydata_hum, 'g-')

canvas_temp = FigureCanvasTkAgg(fig_temp, master=root)
canvas_temp.get_tk_widget().pack()
ani_temp = animation.FuncAnimation(fig_temp, actualizar_grafico, interval=1000)

canvas_hum = FigureCanvasTkAgg(fig_hum, master=root)
canvas_hum.get_tk_widget().pack()
ani_hum = animation.FuncAnimation(fig_hum, actualizar_grafico, interval=1000)

# Iniciar la aplicación de Tkinter
root.mainloop()

# Ejecutar la lectura del sensor en paralelo
async def main():
    await asyncio.gather(control_motor(), lectura_sensor())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
