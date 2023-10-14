import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import asyncio
import matplotlib.pyplot as plt

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

# Funciones para actualizar las gráficas de temperatura y humedad
def update_temperature_plot():
    plt.subplot(211)  # Gráfico superior
    plt.plot(time_data, temperature_data, label='Temperatura (°C)')
    plt.ylabel('Temperatura (°C)')
    plt.legend()

def update_humidity_plot():
    plt.subplot(212)  # Gráfico inferior
    plt.plot(time_data, humidity_data, label='Humedad (%)')
    plt.xlabel('Tiempo (segundos)')
    plt.ylabel('Humedad (%)')
    plt.legend()

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
            # Guardar los datos en las listas
            temperature_data.append(temperature)
            humidity_data.append(humidity)
            time_data.append(time.time())
            # Actualizar las gráficas
            update_temperature_plot()
            update_humidity_plot()
            plt.tight_layout()
            plt.pause(1)
        await asyncio.sleep(1)

async def main():
    await asyncio.gather(control_motor(), lectura_sensor())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    plt.figure()
    plt.ion()  # Habilita el modo interactivo de matplotlib
    plt.subplot(211)  # Gráfico superior para temperatura
    plt.title('Temperatura y Humedad')
    loop.run_until_complete(main())
