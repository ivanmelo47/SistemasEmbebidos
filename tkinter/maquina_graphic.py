import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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

# Función para inicializar la gráfica
def init_plot():
    plt.figure()
    plt.xlabel('Tiempo (segundos)')
    plt.ylabel('Valor')
    plt.legend()

# Función para actualizar la gráfica
def update_plot(i):
    plt.clf()
    plt.plot(time_data, temperature_data, label='Temperatura (°C)')
    plt.plot(time_data, humidity_data, label='Humedad (%)')
    plt.xlabel('Tiempo (segundos)')
    plt.ylabel('Valor')
    plt.legend()

def control_motor_thread():
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
        time.sleep(1)

def lectura_sensor_thread():
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin_dht)
        if humidity is not None and temperature is not None:
            print(f"\rTemperatura: {temperature:.2f}°C, Humedad: {humidity:.2f}%", end="")
            # Guardar los datos en las listas
            temperature_data.append(temperature)
            humidity_data.append(humidity)
            time_data.append(time.time())

def main():
    # Iniciar la gráfica en el hilo principal
    init_plot()
    
    # Crear hilos para el control del motor y la lectura del sensor
    motor_thread = threading.Thread(target=control_motor_thread)
    sensor_thread = threading.Thread(target=lectura_sensor_thread)
    
    # Iniciar los hilos
    motor_thread.start()
    sensor_thread.start()
    
    # Configurar la animación para actualizar la gráfica
    ani = FuncAnimation(plt.gcf(), update_plot, interval=1000)
    
    plt.show()  # Mostrar la gráfica

if __name__ == "__main__":
    main()
