from os import system
from utils import cargar_procesos, inicializar_memoria, worst_fit_asignacion, liberar_particion, mostrar_memoria, mostrar_cola_listos, mostrar_cola_suspendidos
import tkinter as tk
from tkinter import filedialog

def verificar_estructura_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as archivo:
            for linea in archivo:
                elementos = linea.strip().split()
                if len(elementos) != 4:
                    return False
                for elemento in elementos:
                    if not elemento.isdigit():
                        return False
        return True
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return False

def seleccionar_archivo():
    system("cls")
    print("\nSeleccione el archivo que contiene los procesos a simular.")
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    while True:
        archivo_seleccionado = filedialog.askopenfilename(
            title="Selecciona el archivo de procesos",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
        )
        if not archivo_seleccionado:
            print("No se seleccionó ningún archivo. Finalizando la ejecución.")
            return None
        if verificar_estructura_archivo(archivo_seleccionado):
            return archivo_seleccionado
        else:
            print("El archivo seleccionado no tiene la estructura correcta. Por favor, seleccione otro archivo.")

def simulador():
    ruta_archivo = seleccionar_archivo()  # Usar la ventana de selección de archivo
    if not ruta_archivo:
        print("No se seleccionó ningún archivo.")
        return
    memoria = inicializar_memoria()           # Inicializar las particiones de memoria
    tamano_maximo_particion = max(part['tamaño'] for part in memoria)
    procesos = cargar_procesos(ruta_archivo, tamano_maximo_particion)  # Cargar los procesos desde el archivo seleccionado
    cola_listos = []                          # Cola de procesos listos para asignación de memoria (FIFO)
    cola_suspendidos = []                     # Cola de procesos suspendidos
    tiempo_actual = 0                         # Tiempo del sistema
    quantum = 3  # Definimos el quantum
    estadisticas_procesos = []
    procesos_terminados = 0
    proceso_en_ejecucion = None
    quantum_restante = quantum
    system("cls")
    print("\nProcesos a simular:")
    for proceso in procesos:
        print(f"Proceso {proceso['id']} - Tamaño: {proceso['tamaño']}Kb - Arribo: {proceso['arribo']} - Irrupción: {proceso['irrupcion']}")
    print("\nEstado inicial de las particiones de memoria:")
    mostrar_memoria(memoria)
    input("\nPresiona Enter para comenzar la simulación...")

    finalizar = False

    while procesos or cola_listos or cola_suspendidos or any(part['proceso'] for part in memoria):
        print("\nTiempo actual:", tiempo_actual)
        # Extraer todos los procesos cuyo tiempo de arribo es menor o igual al tiempo actual
        procesos_a_arribar = [proceso for proceso in procesos if proceso['arribo'] <= tiempo_actual]
        for proceso in procesos_a_arribar:
            procesos.remove(proceso)
            print(f"Nuevo proceso {proceso['id']} ha arribado en el instante {tiempo_actual}.")
            if worst_fit_asignacion(proceso, memoria):
                print(f"Proceso {proceso['id']} asignado a memoria en el instante {tiempo_actual}.")
                cola_listos.insert(0, proceso)  # Insertar al principio de la cola de listos
            else:
                print(f"Proceso {proceso['id']} no pudo ser asignado a memoria, va a la cola de procesos suspendidos.")
                cola_suspendidos.insert(0, proceso)  # Insertar al principio de la cola de suspendidos

        if proceso_en_ejecucion:
            proceso_en_ejecucion['restante'] -= 1
            quantum_restante -= 1
            print(f"Ejecutando proceso {proceso_en_ejecucion['id']} en el instante {tiempo_actual}, tiempo restante: {proceso_en_ejecucion['restante']}, quantum restante: {quantum_restante}.")
            if proceso_en_ejecucion['restante'] <= 0:
                print(f"Proceso {proceso_en_ejecucion['id']} ha finalizado en el instante {tiempo_actual}.")
                liberar_particion(proceso_en_ejecucion['id'], memoria)
                tiempo_retorno = tiempo_actual - proceso_en_ejecucion['arribo']
                tiempo_espera = tiempo_retorno - proceso_en_ejecucion['irrupcion']
                estadisticas_procesos.append({
                    'id': proceso_en_ejecucion['id'],
                    'TR': tiempo_retorno,
                    'TE': tiempo_espera
                })
                procesos_terminados += 1
                proceso_en_ejecucion = None
                quantum_restante = quantum
                # Intentar asignar procesos suspendidos a memoria
                for i in range(len(cola_suspendidos) - 1, -1, -1):
                    if worst_fit_asignacion(cola_suspendidos[i], memoria):
                        print(f"Proceso {cola_suspendidos[i]['id']} asignado a memoria desde la cola de suspendidos en el instante {tiempo_actual}.")
                        cola_listos.insert(0, cola_suspendidos.pop(i))  # Insertar al principio de la cola de listos
                        break
            elif quantum_restante <= 0:
                print(f"Proceso {proceso_en_ejecucion['id']} alcanzó el quantum, va al inicio de la cola de listos.")
                cola_listos.insert(0, proceso_en_ejecucion)  # Insertar al principio de la cola de listos
                proceso_en_ejecucion = None
                quantum_restante = quantum

        if not proceso_en_ejecucion and cola_listos:
            proceso_en_ejecucion = cola_listos.pop()  # Obtener el último proceso de la cola de listos
            quantum_restante = quantum

        mostrar_memoria(memoria)
        mostrar_cola_listos(cola_listos)
        mostrar_cola_suspendidos(cola_suspendidos)
        
        if not finalizar:
            while True:
                comando = input("\nPresiona Enter para avanzar al siguiente instante o escriba 'final' y presiona Enter para terminar la simulación: ")
                if comando.lower() == "final":
                    finalizar = True
                    break
                elif comando == "":
                    break
                else:
                    print("Comando incorrecto.")
        tiempo_actual += 1

    print("\nSimulación completa.")
    print("\n--- Tiempos de Retorno (TR) y Tiempos de Espera (TE) por proceso ---")
    total_tr = 0
    total_te = 0
    for estadistica in estadisticas_procesos:
        print(f"Proceso {estadistica['id']} - TR: {estadistica['TR']} - TE: {estadistica['TE']}")
        total_tr += estadistica['TR']
        total_te += estadistica['TE']
    
    if procesos_terminados > 0:
        tr_promedio = total_tr / procesos_terminados
        te_promedio = total_te / procesos_terminados
        print(f"\nTiempo de Retorno Promedio: {tr_promedio:.2f}")
        print(f"Tiempo de Espera Promedio: {te_promedio:.2f}")

    if tiempo_actual > 0 and procesos_terminados > 0:
        rendimiento = procesos_terminados / (tiempo_actual - 1)
        print(f"\nInstante final de la simulación: {tiempo_actual - 1} unidades de tiempo.")
        print(f"\nRendimiento del sistema: {rendimiento:.2f} procesos terminados por unidad de tiempo.\n")
    else:
        print("\nNo se pudo calcular el rendimiento del sistema.\n")

if __name__ == "__main__":
    simulador()