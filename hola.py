import adafruit_dht

# Especifica el pin GPIO al que está conectado el sensor (por ejemplo, GPIO 4)
pin = 4

# Crea una instancia del sensor GY-21 en el pin especificado
sensor = adafruit_dht.DHT22(pin)

try:
    # Lee los datos de temperatura y humedad
    temperature_c = sensor.temperature
    humidity = sensor.humidity

    # Imprime los datos
    print(f"Temperatura: {temperature_c}°C")
    print(f"Humedad: {humidity}%")

except RuntimeError as e:
    # En caso de error, muestra un mensaje de error
    print(f"Error de lectura del sensor: {e}")

finally:
    # Libera los recursos del sensor
    sensor.exit()
