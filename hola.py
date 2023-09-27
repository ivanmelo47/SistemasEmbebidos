import smbus2
import time
import RPi.GPIO as GPIO

# Configura los pines GPIO
GPIO.setmode(GPIO.BCM)
SDA_PIN = 27
SCL_PIN = 22
GPIO.setup(SDA_PIN, GPIO.IN)
GPIO.setup(SCL_PIN, GPIO.IN)

# Dirección I2C del sensor GY-21 (puede variar)
address = 0x40

# Inicializar el bus I2C
bus = smbus2.SMBus(1)

# Leer datos de temperatura y humedad
def read_sensor_data():
    data = bus.read_i2c_block_data(address, 0xE5, 2)
    raw_temp = (data[0] << 8) + data[1]
    temperature = ((175.72 * raw_temp) / 65536.0) - 46.85
    return temperature

try:
    while True:
        temp = read_sensor_data()
        print(f"Temperatura: {temp}°C")
        time.sleep(2)  # Esperar 2 segundos antes de la siguiente lectura

except KeyboardInterrupt:
    GPIO.cleanup()  # Limpia los pines GPIO al finalizar
