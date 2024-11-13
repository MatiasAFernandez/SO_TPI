def cargar_procesos(ruta_archivo, tamano_maximo_particion):
    procesos = []
    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            if len(procesos) >= 10:
                break
            id, tamaño, arribo, irrupcion = map(int, linea.strip().split())
            if tamaño <= tamano_maximo_particion:
                procesos.append({'id': id, 'tamaño': tamaño, 'arribo': arribo, 'irrupcion': irrupcion, 'restante': irrupcion})
    return procesos

def inicializar_memoria():
    memoria = [
        {'id': 1, 'inicio': 100, 'tamaño': 250, 'proceso': None, 'fragmentacion': 0},
        {'id': 2, 'inicio': 350, 'tamaño': 150, 'proceso': None, 'fragmentacion': 0},
        {'id': 3, 'inicio': 500, 'tamaño': 50, 'proceso': None, 'fragmentacion': 0}
    ]
    return memoria

def worst_fit_asignacion(proceso, memoria):
    peor_particion = None
    for particion in memoria:
        # Verificar si la partición ya está ocupada por este proceso
        if particion['proceso'] is None and particion['tamaño'] >= proceso['tamaño']:
            if peor_particion is None or particion['tamaño'] > peor_particion['tamaño']:
                peor_particion = particion
    if peor_particion:
        peor_particion['proceso'] = proceso  # Guardar el proceso completo en la partición
        peor_particion['fragmentacion'] = peor_particion['tamaño'] - proceso['tamaño']
        return True
    return False

def liberar_particion(id_proceso, memoria):
    for particion in memoria:
        if particion['proceso'] and particion['proceso']['id'] == id_proceso:
            particion['proceso'] = None
            particion['fragmentacion'] = 0
            return True
    return False

def round_robin(memoria, cola_listos, tiempo_actual, quantum=3):
    proceso_actual = None
    for particion in memoria:
        if particion['proceso']:  # Si hay un proceso en esta partición
            proceso_actual = particion['proceso']  # Obtenemos el proceso completo

            # No descontamos tiempo en el instante 0, solo a partir del instante 1
            if tiempo_actual > 0:
                proceso_actual['restante'] -= 1
                print(f"Ejecutando proceso {proceso_actual['id']} en el instante {tiempo_actual}, tiempo restante: {proceso_actual['restante']}.")

            # Si el proceso ha terminado, liberamos la partición y lo quitamos de la cola de listos
            if proceso_actual['restante'] <= 0:
                print(f"Proceso {proceso_actual['id']} ha finalizado en el instante {tiempo_actual}.")
                liberar_particion(proceso_actual['id'], memoria)

                # Eliminar el proceso de la cola de listos si está presente
                for i, proceso in enumerate(cola_listos):
                    if proceso['id'] == proceso_actual['id']:
                        print(f"Proceso {proceso_actual['id']} eliminado de la cola de listos.")
                        cola_listos.pop(i)
                        break

            # Si el proceso alcanzó el quantum pero no ha terminado, lo movemos al tope de la cola
            elif tiempo_actual > 0 and tiempo_actual % quantum == 0:
                print(f"Proceso {proceso_actual['id']} alcanzó el quantum, va al inicio de la cola de listos.")
                # No volvemos a asignar el proceso a memoria, pero lo reinsertamos en la cola
                if proceso_actual not in cola_listos:
                    cola_listos.insert(0, proceso_actual)  # Lo reinsertamos al tope de la cola
            break
    return proceso_actual

def mostrar_memoria(memoria):
    print("\nTabla de particiones de memoria:")
    headers = ["Partición", "Inicio", "Tamaño", "Proceso", "Fragmentación Interna"]
    print(f"{headers[0]:<10} {headers[1]:<10} {headers[2]:<10} {headers[3]:<10} {headers[4]:<20}")
    print("-" * 60)
    for particion in memoria:
        if particion['proceso']:
            id_proceso = particion['proceso']['id']
        else:
            id_proceso = "Libre"
        print(f"{particion['id']:<10} {particion['inicio']:<10} {particion['tamaño']:<10} {id_proceso:<10} {particion['fragmentacion']:<20}")

def mostrar_cola_listos(cola_listos):
    print("\nCola de procesos listos:")
    for proceso in cola_listos:
        print(f"Proceso {proceso['id']} - Tamaño: {proceso['tamaño']}Kb, Tiempo Restante: {proceso['restante']}")

def mostrar_cola_suspendidos(cola_suspendidos):
    print("\nCola de procesos suspendidos:")
    for proceso in cola_suspendidos:
        print(f"Proceso {proceso['id']} - Tamaño: {proceso['tamaño']}Kb, Tiempo Restante: {proceso['restante']}")