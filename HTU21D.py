import time
import board
import busio
import adafruit_htu21d

# Inicializa el bus I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Inicializa el sensor HTU21D
sensor = adafruit_htu21d.HTU21D(i2c)

while True:
    # Lee la humedad relativa
    humidity = sensor.relative_humidity

    # Lee la temperatura en grados Celsius y Fahrenheit
    temperature_celsius = sensor.temperature
    temperature_fahrenheit = (temperature_celsius * 9 / 5) + 32

    print(f"Relative Humidity : {humidity:.2f} %")
    print(f"Temperature in Celsius : {temperature_celsius:.2f} C")
    print(f"Temperature in Fahrenheit : {temperature_fahrenheit:.2f} F")
    print(" ************************************* ")
    
    time.sleep(1)
