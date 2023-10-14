import RPi.GPIO as GPIO
import dht11
import time
import asyncio

# Configura los pines GPIO y otros valores
pin_dht = 4  # Debes asignar el pin GPIO correcto de la Raspberry Pi
pin_base = 23  # Debes asignar el pin GPIO correcto de la Raspberry Pi

# Define los pines del controlador ULN2003A
IN1 = 17  # Debes asignar el pin GPIO correcto de la Raspberry Pi
IN2 = 18  # Debes asignar el pin GPIO correcto de la Raspberry Pi
IN3 = 27  # Debes asignar el pin GPIO correcto de la Raspberry Pi
IN4 = 22  # Debes asignar el pin GPIO correcto de la Raspberry Pi

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
velocidad_ms = 1
vuelta = True

# Configura el sensor DHT11
instance = dht11.DHT11(pin=pin_dht)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_base, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

async def control_motor():
    global vuelta
    while True:
        result = instance.read()
        if result.is_valid():
            temperature = result.temperature
        else:
            temperature = 0

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
        result = instance.read()
        if result.is_valid():
            temperature = result.temperature
            humidity = result.humidity
            print(f"\rTemperatura: {temperature}°C, Humedad: {humidity}%", end="")
        await asyncio.sleep(1)

async def main():
    await asyncio.gather(control_motor(), lectura_sensor())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
