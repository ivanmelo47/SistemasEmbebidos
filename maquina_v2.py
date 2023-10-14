import RPi.GPIO as GPIO
import Adafruit_DHT
import time

# Configura los pines GPIO
GPIO.setmode(GPIO.BCM)

# Configura el pin GPIO al que está conectado el sensor DHT11
pin_dht = 26

# Configura el pin GPIO que controla el transistor
pin_base = 16

# Define los pines del controlador ULN2003A
IN1 = 2
IN2 = 3
IN3 = 4
IN4 = 5

# Configura los pines del motor
motor_pins = [IN1, IN2, IN3, IN4]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

# Secuencia de pasos para girar el motor en sentido horario
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

# Secuencia de pasos para girar el motor en sentido antihorario (inversa de CW)
sequence_ccw = list(reversed(sequence_cw))

# Calcula el número de pasos para una vuelta completa (360 grados)
pasos_por_vuelta = 510  # Esto es para el motor 28BYJ-48

# Define la velocidad (ajusta este valor para cambiar la velocidad)
velocidad_ms = 1  # Tiempo de espera en milisegundos entre pasos (mayor valor = menor velocidad)

# Verifica si ya se dio la vuelta del actuador
vuelta = True

# Función para activar el relé (encender la carga)
def activar_rele():
    GPIO.output(pin_base, GPIO.HIGH)

# Función para desactivar el relé (apagar la carga)
def desactivar_rele():
    GPIO.output(pin_base, GPIO.LOW)

try:
    # Configura el pin del relé
    GPIO.setup(pin_base, GPIO.OUT)
    desactivar_rele()

    while True:
        # Lee datos del sensor DHT11
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin_dht)
        
        # Imprime los datos leídos
        if humidity is not None and temperature is not None:
            print(f"Temperatura: {temperature:.2f}°C, Humedad: {humidity:.2f}%")
        
            # Verifica si la temperatura es mayor a 30 grados
            if humidity >= 56:
                # Gira el motor en sentido horario para una vuelta completa
                if vuelta:
                    vuelta = False
                    for _ in range(pasos_por_vuelta):
                        for step in sequence_cw:
                            for i in range(4):
                                GPIO.output(motor_pins[i], step[i])
                            time.sleep(velocidad_ms)
                
                    # Enciende el Ventilador
                    activar_rele()
                else:
                    # Gira el motor en sentido antihorario para una vuelta completa
                    vuelta = True
                    # Apaga el Ventilador
                    desactivar_rele()
                    for _ in range(pasos_por_vuelta):
                        for step in sequence_ccw:
                            for i in range(4):
                                GPIO.output(motor_pins[i], step[i])
                            time.sleep(velocidad_ms)
        
        # Espera 1 segundo antes de la próxima lectura
        time.sleep(1)
except Exception as e:
    print("Error al leer el sensor:", e)
finally:
    GPIO.cleanup()
