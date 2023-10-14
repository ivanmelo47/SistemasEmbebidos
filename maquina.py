import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import asyncio

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
velocidad_ms = 1
vuelta = True

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
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin_dht)
        
        if humidity is not None and temperature is not None:
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
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin_dht)
        if humidity is not None and temperature is not None:
            print(f"\rTemperatura: {temperature:.2f}°C, Humedad: {humidity:.2f}%", end="")
        await asyncio.sleep(1)

async def main():
    await asyncio.gather(control_motor(), lectura_sensor())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
