# Simulador de Gestión de Memoria

## Descripción
Este proyecto implementa un simulador de gestión de memoria que utiliza algoritmos de asignación de memoria como el *Worst Fit* y planificación de procesos con *Round Robin*. Simula el comportamiento del sistema de memoria y procesos dentro de un sistema operativo.

## Requisitos Previos
```
- Python 3.11 o superior
- No requiere dependencias adicionales
```

## Instalación
1. Clona este repositorio:
```bash
git clone https://github.com/MatiasAFernandez/SO_TPI.git
```

## Uso
1. Al iniciar el simulador, se cargan los procesos desde el archivo `procesos.txt`.
2. Se puede visualizar el estado de la memoria y la cola de procesos en cada instante de tiempo.
3. Al finalizar, se muestran estadísticas como los tiempos de retorno y espera por proceso.

## Comandos
Para ejecutar el programa, simplemente ejecuta:
```bash
 python main.py
```
## Formato de Entrada
El archivo `procesos.txt` debe tener el siguiente formato:

'id tamaño arribo irrupcion'

'id': identificador del proceso
'tamaño': Tamaño en KB del proceso 
'arribo': Tiempo de llegada del proceso al sistema
'irrupcion': Tiempo de ejecución requerido por el proceso

Cada uno de los atributos son expresados con numeros naturales. Ejemplo:
El proceso uno apareceria como:
1 80 0 5
Donde 1 es el id del proceso, 80 es el tamaño en Kb que ocupará en meoria, 
0 es el tiempo de arribo y 5 es el tiempo de irrupción.

Cada linea del archivo representa un proceso.
No puede haber mas de 10 lineas ya que ese es el tope de procesos aceptados en cada procesamiento.

## Aclaraciones
Los proceso cuyo tamaño sean mayores al de la partición de mayor tamaño serán descartados y no formarán
parte de los procesos a simular.
Si la cantidad de procesos dentro del archivo leido superan los 10 procesos, solo se tendran en cuenta los
primeros 10 procesos.

## Autores Grupo LIKE A PLAYER
```
-Altamirano Alejandro
-Fernandez Matias
-Judkevich Natasha Nicole
-Maldonado Leandro
-Ramirez Rocio
```

## Estado del Proyecto
El proyecto está en desarrollo, se planea agregar más funcionalidades en el futuro.

