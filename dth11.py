import Adafruit_DHT

# Configura el modelo del sensor y el número de pin GPIO
sensor = Adafruit_DHT.DHT11
pin = 4

try:
    # Intenta leer los datos del sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        print(f"Temperatura: {temperature:.2f}°C")
        print(f"Humedad: {humidity:.2f}%")
    else:
        print("Error al leer el sensor. Revisa la conexión y vuelve a intentar.")
except Exception as e:
    print(f"Error: {str(e)}")
