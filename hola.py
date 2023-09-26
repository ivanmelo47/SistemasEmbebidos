import tkinter as tk

# Función para mostrar un mensaje cuando se hace clic en el botón
def mostrar_mensaje():
    etiqueta.config(text="Hola, has hecho clic en el botón")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Ejemplo de Interfaz con Tkinter")

# Crear una etiqueta
etiqueta = tk.Label(ventana, text="¡Bienvenido a Tkinter!")
etiqueta.pack(pady=10)

# Crear un botón
boton = tk.Button(ventana, text="Haz clic", command=mostrar_mensaje)
boton.pack()

# Iniciar el bucle principal
ventana.mainloop()
