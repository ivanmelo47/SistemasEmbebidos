import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import asyncio
import matplotlib.pyplot as plt

# Resto del código ...

# Variables para verificar si las gráficas se han configurado
temperature_plot_configured = False
humidity_plot_configured = False

# Funciones para actualizar las gráficas de temperatura y humedad
def update_temperature_plot():
    plt.subplot(2, 1, 1)  # Subgráfico 1 (temperatura)
    plt.plot(time_data, temperature_data, label='Temperatura (°C)')
    plt.xlabel('Tiempo (segundos)')
    plt.ylabel('Temperatura (°C)')
    plt.legend()
    temperature_plot_configured = True  # Marcar como configurado

def update_humidity_plot():
    plt.subplot(2, 1, 2)  # Subgráfico 2 (humedad)
    plt.plot(time_data, humidity_data, label='Humedad (%)')
    plt.xlabel('Tiempo (segundos)')
    plt.ylabel('Humedad (%)')
    plt.legend()
    humidity_plot_configured = True  # Marcar como configurado

# Función para actualizar la gráfica
def update_plot():
    if not temperature_plot_configured:
        update_temperature_plot()
    if not humidity_plot_configured:
        update_humidity_plot()
    plt.tight_layout()  # Ajustar automáticamente el espaciado
    plt.pause(1)

# Resto del código ...

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    plt.ion()  # Habilita el modo interactivo de matplotlib
    plt.figure(figsize=(8, 6))  # Tamaño de la figura (ancho, alto)
    loop.run_until_complete(main())
