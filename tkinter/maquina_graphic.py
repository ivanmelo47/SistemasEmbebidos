import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import asyncio
import matplotlib.pyplot as plt

# ... (resto del código como está)

# Listas para almacenar datos de temperatura y humedad
temperature_data = []
humidity_data = []
time_data = []

# Función para actualizar la gráfica
def update_plot():
    plt.clf()
    plt.plot(time_data, temperature_data, label='Temperatura (°C)')
    plt.plot(time_data, humidity_data, label='Humedad (%)')
    plt.xlabel('Tiempo (segundos)')
    plt.ylabel('Valor')
    plt.legend()
    plt.pause(1)

async def control_motor():
    # ... (código del motor como está)

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

async def main():
    await asyncio.gather(control_motor(), lectura_sensor())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    plt.ion()  # Habilita el modo interactivo de matplotlib
    plt.figure()
    loop.run_until_complete(main())
