import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import asyncio
import matplotlib.pyplot as plt
from tkinter import *

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

# Configuración de los pines GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_base, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Listas para almacenar datos de temperatura y humedad
temperature_data = []
humidity_data = []
time_data = []

# Variable para controlar el estado del sistema
sistema_en_ejecucion = False

# Función para actualizar la gráfica con etiquetas numéricas
def update_plot():
    plt.clf()
    plt.plot(time_data, temperature_data, label='Temperatura (°C)')
    plt.plot(time_data, humidity_data, label='Humedad (%)')
    plt.xlabel('Tiempo (segundos)')
    plt.ylabel('Valor')
    
    # Agregar etiquetas numéricas
    if temperature_data:
        plt.text(time_data[-1], temperature_data[-1], f'{temperature_data[-1]:.2f}°C', ha='right', va='bottom')
    if humidity_data:
        plt.text(time_data[-1], humidity_data[-1], f'{humidity_data[-1]:.2f}%', ha='right', va='top')

    plt.legend()
    plt.pause(1)

async def control_motor():
    global vuelta
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin_dht)
        
        if humidity is not None and temperature is not None:
            if vuelta and temperature >= 26:
                for _ in range(pasos_por_vuelta):
                    for step in sequence_cw:
                        GPIO.output(IN1, step[0])
                        GPIO.output(IN2, step[1])
                        GPIO.output(IN3, step[2])
                        GPIO.output(IN4, step[3])
                        await asyncio.sleep(velocidad_ms)
                GPIO.output(pin_base, GPIO.HIGH)
                vuelta = False
            elif not vuelta and temperature < 26:
                for _ in range(pasos_por_vuelta):
                    for step in sequence_ccw:
                        GPIO.output(IN1, step[0])
                        GPIO.output(IN2, step[1])
                        GPIO.output(IN3, step[2])
                        GPIO.output(IN4, step[3])
                        await asyncio.sleep(velocidad_ms)
                GPIO.output(pin_base, GPIO.LOW)
                vuelta = True
        await asyncio.sleep(1)

async def lectura_sensor():
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin_dht)
        if humidity is not None and temperature is not None:
            print(f"\rTemperatura: {temperature:.2f}°C, Humedad: {humidity:.2f}%", end="")
            # Guardar los datos en las listas
            temperature_data.append(temperature)
            humidity_data.append(humidity)
            time_data.append(time.time())
            # Actualizar la gráfica
            update_plot()
        await asyncio.sleep(1)

# Función para iniciar/reanudar el sistema
def iniciar_sistema():
    global sistema_en_ejecucion
    if not sistema_en_ejecucion:
        sistema_en_ejecucion = True
        loop.create_task(main())  # Iniciar el sistema en segundo plano

# Función para detener el sistema
def detener_sistema():
    global sistema_en_ejecucion
    sistema_en_ejecucion = False

# Función para cerrar la aplicación
def cerrar_aplicacion():
    detener_sistema()
    root.quit()

# Crear una ventana de tkinter
root = Tk()
root.title("Control del Sistema")

# Botones en la parte superior
frame_top = Frame(root)
frame_top.pack(side=TOP)

boton_iniciar = Button(frame_top, text="Iniciar/Reanudar Sistema", command=iniciar_sistema)
boton_detener = Button(frame_top, text="Detener Sistema", command=detener_sistema)
boton_cerrar = Button(frame_top, text="Cerrar Aplicación", command=cerrar_aplicacion)

boton_iniciar.pack(side=LEFT)
boton_detener.pack(side=LEFT)
boton_cerrar.pack(side=LEFT)

# Gráfica
plt.ion()  # Habilita el modo interactivo de matplotlib
plt.figure()

# Loop principal de la aplicación
root.mainloop()
