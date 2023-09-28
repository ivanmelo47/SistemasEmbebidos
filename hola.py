import smbus
import time

# Dirección I2C del sensor GY-21 (HTU21D)
sensor_address = 0x40

# Inicializa el bus I2C (puedes usar 0 o 1, dependiendo de tu Raspberry Pi)
bus = smbus.SMBus(1)

# Comando para leer la temperatura (sin resolución adicional)
bus.write_byte(sensor_address, 0xF3)

# Espera un momento para que el sensor realice la medición
time.sleep(0.5)

# Lee 2 bytes de datos de temperatura
data = bus.read_i2c_block_data(sensor_address, 0x00, 2)

# Calcula la temperatura
temp_raw = (data[0] << 8) + data[1]
temp = -46.85 + (175.72 * temp_raw / 65536.0)

# Imprime la temperatura en Celsius
print(f"Temperatura: {temp:.2f} °C")
