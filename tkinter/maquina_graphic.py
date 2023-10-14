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

async def control_motor():
    global vuelta
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin_dht)
        
        if humidity is not None and temperature is not None:
            if temperature >= 26:
                if vuelta:
                    for _ in range(pasos_por_vuelta):
                        for step in sequence_cw:
                            GPIO.output(IN1, step[0])
                            GPIO.output(IN2, step[1])
                            GPIO.output(IN3, step[2])
                            GPIO.output(IN4, step[3])
                            time.sleep(velocidad_ms)
                    GPIO.output(pin_base, GPIO.HIGH)
                    vuelta = False
                else:
                    if not vuelta:
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

# Código para crear la ventana de tkinter y los gráficos
def crear_actualizar_grafico_temp():
    global xdata_temp, ydata_temp, line_temp
    xdata_temp.append(time.time())
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin_dht)
    if humidity is not None and temperature is not None:
        ydata_temp.append(temperature)
    if len(xdata_temp) > 20:
        xdata_temp.pop(0)
        ydata_temp.pop(0)
    line_temp.set_data(xdata_temp, ydata_temp)
    ax_temp.relim()
    ax_temp.autoscale_view()

def crear_actualizar_grafico_hum():
    global xdata_hum, ydata_hum, line_hum
    xdata_hum.append(time.time())
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin_dht)
    if humidity is not None and temperature is not None:
        ydata_hum.append(humidity)
    if len(xdata_hum) > 20:
        xdata_hum.pop(0)
        ydata_hum.pop(0)
    line_hum.set_data(xdata_hum, ydata_hum)
    ax_hum.relim()
    ax_hum.autoscale_view()

def iniciar_graficos():
    global adquirir_datos, ani, loop
    adquirir_datos = True
    loop = asyncio.get_event_loop()
    loop.create_task(control_motor())  # Llama a control_motor para mover el motor
    ani.event_source.start()  # Inicia la animación de los gráficos

def detener_graficos():
    global adquirir_datos, ani, loop
    adquirir_datos = False
    ani.event_source.stop()  # Detiene la animación de los gráficos
    loop.stop()  # Detiene el bucle de eventos de asyncio

root = tk.Tk()
root.title("Sensor DHT11 - Gráficos de Temperatura y Humedad")

frame_temp = ttk.Frame(root)
frame_temp.grid(column=0, row=0, padx=10, pady=10)
frame_temp.grid_propagate(0)

frame_hum = ttk.Frame(root)
frame_hum.grid(column=1, row=0, padx=10, pady=10)
frame_hum.grid_propagate(0)

iniciar_button = ttk.Button(root, text="Iniciar Gráficos", command=iniciar_graficos)
iniciar_button.grid(row=1, column=0, columnspan=2)

detener_button = ttk.Button(root, text="Detener Gráficos", command=detener_graficos)
detener_button.grid(row=2, column=0, columnspan=2)

fig_temp = Figure(figsize=(5, 4), dpi=100)
ax_temp = fig_temp.add_subplot(111)
ax_temp.set_xlabel('Tiempo (s)')
ax_temp.set_ylabel('Temperatura (°C)')
xdata_temp, ydata_temp = [], []
line_temp, = ax_temp.plot(xdata_temp, ydata_temp, 'r-')

canvas_temp = FigureCanvasTkAgg(fig_temp, master=frame_temp)
canvas_temp.get_tk_widget().grid(row=0, column=0)
ani_temp = animation.FuncAnimation(fig_temp, crear_actualizar_grafico_temp, blit=False, interval=1000)

fig_hum = Figure(figsize=(5, 4), dpi=100)
ax_hum = fig_hum.add_subplot(111)
ax_hum.set_xlabel('Tiempo (s)')
ax_hum.set_ylabel('Humedad (%)')
xdata_hum, ydata_hum = [], []
line_hum, = ax_hum.plot(xdata_hum, ydata_hum, 'b-')

canvas_hum = FigureCanvasTkAgg(fig_hum, master=frame_hum)
canvas_hum.get_tk_widget().grid(row=0, column=0)
ani_hum = animation.FuncAnimation(fig_hum, crear_actualizar_grafico_hum, blit=False, interval=1000)

adquirir_datos = False

root.mainloop()
