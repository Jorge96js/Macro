import tkinter as tk
import pyautogui
import pyperclip
import pyclip
import json



# Lista para mantener referencias a los botones de inicio y pasos agregados
botones_iniciar = []
pasos_agregados = []


def iniciar_accion(x, y, tiempo_entre_clics, accion=None):
    try:
        x = int(x)
        y = int(y)
        tiempo_entre_clics = float(tiempo_entre_clics) / 1000  # Convertir a segundos
        pyautogui.click(x, y, interval=tiempo_entre_clics)

        # Realizar la acción de copiar o pegar si se especifica
        if accion == "copiar":
            copiar_nombre_archivo()
        elif accion == "pegar":
            pegar_texto()
    except ValueError:
        resultado.config(text="¡Error! Introduce coordenadas y tiempo válidos.")


def agregar_paso():
    # Obtener las coordenadas y el tiempo entre clics ingresados
    x = entry_x.get()
    y = entry_y.get()
    tiempo_entre_clics = entry_tiempo_entre_clics.get()

    # Validar que las coordenadas y el tiempo sean válidos
    try:
        x = int(x)
        y = int(y)
        tiempo_entre_clics = float(tiempo_entre_clics)
    except ValueError:
        resultado.config(text="¡Error! Introduce coordenadas y tiempo válidos.")
        return

    # Determinar la acción a realizar
    accion = None
    if accion_copiar.get():
        accion = "copiar"
    elif accion_pegar.get():
        accion = "pegar"

    # Agregar el paso a la lista y actualizar la interfaz
    pasos_agregados.append((x, y, tiempo_entre_clics, accion))
    actualizar_lista_pasos()


def actualizar_lista_pasos():
    lista_pasos.delete(0, tk.END)
    for i, paso in enumerate(pasos_agregados, start=1):
        descripcion_accion = ""
        if paso[3] == "copiar":
            descripcion_accion = " (Copiar nombre de archivo)"
        elif paso[3] == "pegar":
            descripcion_accion = " (Pegar nombre de archivo)"
        lista_pasos.insert(tk.END, f"Paso {i}: ({paso[0]}, {paso[1]}), Tiempo: {paso[2]} ms{descripcion_accion}")


def iniciar_todas_las_acciones():
    for paso in pasos_agregados:
        iniciar_accion(paso[0], paso[1], paso[2], paso[3])


def actualizar_coordenadas():
    x, y = pyautogui.position()
    coordenadas.config(text=f"X: {x}, Y: {y}")
    ventana.after(100, actualizar_coordenadas)


def tu_funcion_de_loop():
    # Lógica para reiniciar el programa desde cero
    while True:  # Bucle infinito
        for paso in pasos_agregados:
            iniciar_accion(paso[0], paso[1], paso[2])


# Función para copiar el nombre del archivo seleccionado
def copiar_nombre_archivo():
    try:

        pyautogui.hotkey('f2')
        pyautogui.hotkey('ctrl','c')

        pyperclip.copy()
        time.sleep(0.5)  # Esperar 0.5 segundos
        nombre_archivo = pyperclip.paste()  # Obtener el texto copiado del portapapeles
        resultado.config(text=f"Nombre del archivo copiado: {nombre_archivo}")
    except Exception as e:
        resultado.config(text=f"¡Error al copiar el nombre del archivo: {e}")

def pegar_texto():
    try:
        name = pyperclip.paste()
        pyautogui.hotkey('ctrl', 'v')  # Obtener el nombre del archivo desde el portapapeles

        pyautogui.write(name)
        print(name)  # Imprimir el nombre del archivo (opcional)
        resultado.config(text="Texto pegado. {name}")
    except Exception as e:
        resultado.config(text=f"¡Error al pegar el texto: {e}")


def guardar_configuracion():
    configuracion = {
        "pasos_agregados": pasos_agregados,
        "entry_x": entry_x.get(),
        "entry_y": entry_y.get(),
        "entry_tiempo_entre_clics": entry_tiempo_entre_clics.get(),
        "accion_copiar": accion_copiar.get(),
        "accion_pegar": accion_pegar.get()
    }
    with open("configuracion.json", "w") as archivo:
        json.dump(configuracion, archivo)
    resultado.config(text="Configuración guardada.")

def cargar_configuracion():
    try:
        with open("configuracion.json", "r") as archivo:
            configuracion = json.load(archivo)
        global pasos_agregados
        pasos_agregados = configuracion["pasos_agregados"]
        entry_x.delete(0, tk.END)
        entry_x.insert(0, configuracion["entry_x"])
        entry_y.delete(0, tk.END)
        entry_y.insert(0, configuracion["entry_y"])
        entry_tiempo_entre_clics.delete(0, tk.END)
        entry_tiempo_entre_clics.insert(0, configuracion["entry_tiempo_entre_clics"])
        accion_copiar.set(configuracion["accion_copiar"])
        accion_pegar.set(configuracion["accion_pegar"])
        actualizar_lista_pasos()
        resultado.config(text="Configuración cargada.")
    except FileNotFoundError:
        resultado.config(text="No se encontró el archivo de configuración.")
    except Exception as e:
        resultado.config(text=f"¡Error al cargar la configuración: {e}")


# Crear la ventana
ventana = tk.Tk()
ventana.title("Automatización de Clicks")

# Checks para copiar y pegar
accion_copiar = tk.BooleanVar()
accion_pegar = tk.BooleanVar()

# Botón para guardar la configuración
boton_guardar_config = tk.Button(ventana, text="Guardar Configuración", command=guardar_configuracion)
boton_guardar_config.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

# Botón para cargar la configuración
boton_cargar_config = tk.Button(ventana, text="Cargar Configuración", command=cargar_configuracion)
boton_cargar_config.grid(row=11, column=0, columnspan=2, padx=10, pady=5)


# Crear etiquetas y campos de entrada para las coordenadas
etiqueta_x = tk.Label(ventana, text="Coordenada X:")
etiqueta_x.grid(row=0, column=0, padx=10, pady=5)
entry_x = tk.Entry(ventana)
entry_x.grid(row=0, column=1, padx=10, pady=5)

etiqueta_y = tk.Label(ventana, text="Coordenada Y:")
etiqueta_y.grid(row=1, column=0, padx=10, pady=5)
entry_y = tk.Entry(ventana)
entry_y.grid(row=1, column=1, padx=10, pady=5)

# Etiqueta y campo de entrada para el tiempo entre clics
etiqueta_tiempo_entre_clics = tk.Label(ventana, text="Tiempo entre clics (ms):")
etiqueta_tiempo_entre_clics.grid(row=2, column=0, padx=10, pady=5)
entry_tiempo_entre_clics = tk.Entry(ventana)
entry_tiempo_entre_clics.grid(row=2, column=1, padx=10, pady=5)

# Botón para agregar pasos
boton_agregar_paso = tk.Button(ventana, text="Agregar Paso", command=agregar_paso)
boton_agregar_paso.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# Lista para mostrar los pasos agregados
lista_pasos = tk.Listbox(ventana, width=50, height=10)
lista_pasos.grid(row=4, column=0, columnspan=2, padx=10, pady=5)


# Botón para iniciar todas las acciones
boton_iniciar_todo = tk.Button(ventana, text="Iniciar Todo", command=iniciar_todas_las_acciones)
boton_iniciar_todo.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

# Check buttons para copiar y pegar
check_copiar = tk.Checkbutton(ventana, text="Copiar nombre del archivo", variable=accion_copiar, onvalue=True, offvalue=False, command=lambda: accion_pegar.set(False))
check_copiar.grid(row=6, column=0, padx=10, pady=5)
# Check buttons para copiar y pegar
check_copiar = tk.Checkbutton(ventana, text="Copiar texto seleccionado", variable=accion_copiar, onvalue=True, offvalue=False, command=lambda: accion_pegar.set(False))
check_copiar.grid(row=6, column=0, padx=10, pady=5)

check_pegar = tk.Checkbutton(ventana, text="Pegar texto", variable=accion_pegar, onvalue=True, offvalue=False, command=lambda: accion_copiar.set(False))
check_pegar.grid(row=6, column=1, padx=10, pady=5)

# Etiqueta para mostrar coordenadas del mouse
coordenadas = tk.Label(ventana, text="X: 0, Y: 0")
coordenadas.grid(row=7, column=0, columnspan=2)

# Crear el botón de loop
boton_loop = tk.Button(ventana, text="Loop", command=tu_funcion_de_loop)
boton_loop.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

# Etiqueta para mostrar resultados
resultado = tk.Label(ventana, text="")
resultado.grid(row=9, column=0, columnspan=2)

# Actualizar las coordenadas del mouse en tiempo real
actualizar_coordenadas()

# Iniciar el bucle principal de la ventana
ventana.mainloop()