from os import system
from utils import cargar_procesos, inicializar_memoria, worst_fit_asignacion, liberar_particion, mostrar_memoria, mostrar_cola_listos

def simulador():
    procesos = cargar_procesos('procesos.txt')  # Cargar los procesos desde el archivo
    memoria = inicializar_memoria()             # Inicializar las particiones de memoria
    cola_listos = []                            # Cola de procesos listos para asignación de memoria (FIFO)
    tiempo_actual = 0                           # Tiempo del sistema

    #Definimos el quantum
    quantum = 3

    # Obtener el tamaño de la partición más grande
    tamano_maximo_particion = max(part['tamaño'] for part in memoria)

    # Lista para guardar estadísticas por proceso (id, TR, TE)
    estadisticas_procesos = []
    procesos_terminados = 0  # Lleva el conteo de procesos terminados

    system("cls")
    print("\nEstado inicial de las particiones de memoria:")
    mostrar_memoria(memoria)  # Mostrar particiones vacías
    input("\nPresiona Enter para comenzar la simulación...")

    while procesos or cola_listos or any(part['proceso'] for part in memoria):  # Continuar mientras haya procesos o memoria ocupada
        print("\nTiempo actual:", tiempo_actual)

        # Agregar nuevos procesos a la cola de listos según el tiempo de arribo
        while procesos and procesos[0]['arribo'] <= tiempo_actual:
            proceso = procesos.pop(0)

            # Verificar si el tamaño del proceso es mayor que la partición más grande
            if proceso['tamaño'] > tamano_maximo_particion:
                print(f"Proceso {proceso['id']} eliminado: tamaño {proceso['tamaño']}K es mayor que cualquier partición disponible.")
                continue  # El proceso se descarta y no se añade a la cola

            print(f"Nuevo proceso {proceso['id']} ha arribado en el instante {tiempo_actual}.")
            # Intentamos asignar la memoria
            if worst_fit_asignacion(proceso, memoria):
                print(f"Proceso {proceso['id']} asignado a memoria en el instante {tiempo_actual}.")
            else:
                print(f"Proceso {proceso['id']} no pudo ser asignado a memoria.")
            # Siempre añadimos el proceso al tope de la cola de listos
            cola_listos.insert(0, proceso)

        # El proceso que está al fondo de la cola debe ejecutarse (si tiene una partición asignada)
        if cola_listos:
            proceso_actual = cola_listos[-1]  # Proceso al fondo de la cola

            # Si tiene una partición asignada, lo ejecutamos
            if any(part['proceso'] == proceso_actual for part in memoria):
                if tiempo_actual > 0:
                    proceso_actual['restante'] -= 1
                print(f"Ejecutando proceso {proceso_actual['id']} en el instante {tiempo_actual}, tiempo restante: {proceso_actual['restante']}.")

                # Si el proceso terminó, calculamos TR, TE y liberamos la memoria
                if proceso_actual['restante'] <= 0:
                    print(f"Proceso {proceso_actual['id']} ha finalizado en el instante {tiempo_actual}.")
                    liberar_particion(proceso_actual['id'], memoria)
                    cola_listos.pop()  # Eliminar del fondo de la cola

                    # Cálculo de métricas TR, TE y actualización de procesos terminados
                    tiempo_retorno = tiempo_actual - proceso_actual['arribo']
                    tiempo_espera = tiempo_retorno - proceso_actual['irrupcion']
                    
                    # Guardar las estadísticas del proceso
                    estadisticas_procesos.append({
                        'id': proceso_actual['id'],
                        'TR': tiempo_retorno,
                        'TE': tiempo_espera
                    })
                    procesos_terminados += 1  # Incrementar contador de procesos terminados

                # Si el quantum se agotó y el proceso sigue, lo movemos al tope de la cola
                elif tiempo_actual > 0 and int(proceso_actual['restante']) + quantum == int(proceso_actual['irrupcion']):
                    print(f"Proceso {proceso_actual['id']} alcanzó el quantum, va al tope de la cola.")
                    cola_listos.insert(0, cola_listos.pop())  # Mover al tope de la cola

            # Si no tiene partición asignada, lo intentamos asignar
            else:
                if worst_fit_asignacion(proceso_actual, memoria):
                    print(f"Proceso {proceso_actual['id']} asignado a memoria en el instante {tiempo_actual}.")
                else:
                    # No pudo ser asignado, lo movemos al tope de la cola
                    print(f"Proceso {proceso_actual['id']} no pudo ser asignado a memoria, va al tope de la cola.")
                    cola_listos.insert(0, cola_listos.pop())  # Mover al tope de la cola

        # Mostrar el estado actual de la memoria y la cola de listos
        mostrar_memoria(memoria)
        mostrar_cola_listos(cola_listos)

        # Avanzar la simulación solo cuando el usuario presione Enter
        input("\nPresiona Enter para avanzar al siguiente instante...")

        # Incrementar el tiempo del sistema
        tiempo_actual += 1

    # Generar informe al finalizar la simulación
    print("\nSimulación completa.")

    # Mostrar tiempos de retorno y espera para cada proceso
    print("\n--- Tiempos de Retorno (TR) y Tiempos de Espera (TE) por proceso ---")
    for estadistica in estadisticas_procesos:
        print(f"Proceso {estadistica['id']} - TR: {estadistica['TR']} - TE: {estadistica['TE']}")

    # Calcular y mostrar rendimiento del sistema
    if tiempo_actual > 0 and procesos_terminados > 0:
        rendimiento = procesos_terminados / tiempo_actual
        print(f"\nRendimiento del sistema: {rendimiento:.2f} procesos terminados por unidad de tiempo.\n")
    else:
        print("\nNo se pudo calcular el rendimiento del sistema (no hay procesos terminados o tiempo insuficiente).\n")

if __name__ == "__main__":
    simulador()
