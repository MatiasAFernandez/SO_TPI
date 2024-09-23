from os import system
from utils import cargar_procesos, inicializar_memoria, worst_fit_asignacion, liberar_particion, mostrar_memoria, mostrar_cola_listos
import tkinter as tk
from tkinter import filedialog

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    archivo_seleccionado = filedialog.askopenfilename(
        title="Selecciona el archivo de procesos",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )
    return archivo_seleccionado

def simulador():
    ruta_archivo = seleccionar_archivo()  # Usar la ventana de selección de archivo
    if not ruta_archivo:
        print("No se seleccionó ningún archivo.")
        return

    procesos = cargar_procesos(ruta_archivo)  # Cargar los procesos desde el archivo seleccionado
    memoria = inicializar_memoria()           # Inicializar las particiones de memoria
    cola_listos = []                          # Cola de procesos listos para asignación de memoria (FIFO)
    tiempo_actual = 0                         # Tiempo del sistema

    quantum = 3  # Definimos el quantum
    tamano_maximo_particion = max(part['tamaño'] for part in memoria)

    estadisticas_procesos = []
    procesos_terminados = 0

    system("cls")
    print("\nEstado inicial de las particiones de memoria:")
    mostrar_memoria(memoria)
    input("\nPresiona Enter para comenzar la simulación...")

    while procesos or cola_listos or any(part['proceso'] for part in memoria):
        print("\nTiempo actual:", tiempo_actual)

        while procesos and procesos[0]['arribo'] <= tiempo_actual:
            proceso = procesos.pop(0)
            if proceso['tamaño'] > tamano_maximo_particion:
                print(f"Proceso {proceso['id']} eliminado: tamaño {proceso['tamaño']}K es mayor que cualquier partición disponible.")
                continue

            print(f"Nuevo proceso {proceso['id']} ha arribado en el instante {tiempo_actual}.")
            if worst_fit_asignacion(proceso, memoria):
                print(f"Proceso {proceso['id']} asignado a memoria en el instante {tiempo_actual}.")
            else:
                print(f"Proceso {proceso['id']} no pudo ser asignado a memoria.")
            cola_listos.insert(0, proceso)

        if cola_listos:
            proceso_actual = cola_listos[-1]
            if any(part['proceso'] == proceso_actual for part in memoria):
                if tiempo_actual > 0:
                    proceso_actual['restante'] -= 1
                print(f"Ejecutando proceso {proceso_actual['id']} en el instante {tiempo_actual}, tiempo restante: {proceso_actual['restante']}.")

                if proceso_actual['restante'] <= 0:
                    print(f"Proceso {proceso_actual['id']} ha finalizado en el instante {tiempo_actual}.")
                    liberar_particion(proceso_actual['id'], memoria)
                    cola_listos.pop()

                    tiempo_retorno = tiempo_actual - proceso_actual['arribo']
                    tiempo_espera = tiempo_retorno - proceso_actual['irrupcion']

                    estadisticas_procesos.append({
                        'id': proceso_actual['id'],
                        'TR': tiempo_retorno,
                        'TE': tiempo_espera
                    })
                    procesos_terminados += 1
                elif tiempo_actual > 0 and int(proceso_actual['restante']) + quantum == int(proceso_actual['irrupcion']):
                    print(f"Proceso {proceso_actual['id']} alcanzó el quantum, va al tope de la cola.")
                    cola_listos.insert(0, cola_listos.pop())
            else:
                if worst_fit_asignacion(proceso_actual, memoria):
                    print(f"Proceso {proceso_actual['id']} asignado a memoria en el instante {tiempo_actual}.")
                else:
                    print(f"Proceso {proceso_actual['id']} no pudo ser asignado a memoria, va al tope de la cola.")
                    cola_listos.insert(0, cola_listos.pop())

        mostrar_memoria(memoria)
        mostrar_cola_listos(cola_listos)
        input("\nPresiona Enter para avanzar al siguiente instante...")
        tiempo_actual += 1

    print("\nSimulación completa.")
    print("\n--- Tiempos de Retorno (TR) y Tiempos de Espera (TE) por proceso ---")
    for estadistica in estadisticas_procesos:
        print(f"Proceso {estadistica['id']} - TR: {estadistica['TR']} - TE: {estadistica['TE']}")

    if tiempo_actual > 0 and procesos_terminados > 0:
        rendimiento = procesos_terminados / tiempo_actual
        print(f"\nRendimiento del sistema: {rendimiento:.2f} procesos terminados por unidad de tiempo.\n")
    else:
        print("\nNo se pudo calcular el rendimiento del sistema.\n")

if __name__ == "__main__":
    simulador()
