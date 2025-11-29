
# Airbnb 🏡


Se desarrolló un sistema de control de asistencia orientado a la gestión administrativa de personal. El proyecto permite registrar entradas y salidas de empleados, contabilizar los días trabajados y mostrar los resultados en una interfaz organizada. Incluye una lógica de cortes históricos que facilita generar reportes acumulativos desde la última fecha registrada hasta el día actual. Los reportes se presentan de forma clara y se exportan automáticamente en archivos organizados, lo que optimiza procesos internos, reduce tiempos de elaboración manual y asegura la integridad de la información.


## 📡​ Tecnologías utilizadas


Python – desarrollo de la lógica principal del sistema

Tkinter – creación de la interfaz gráfica con tablas y botones

SQLite – gestión de la base de datos y almacenamiento de registros

SQL – consultas para contabilizar días trabajados y generar reportes

Archivos TXT – exportación automática de reportes organizados
## ✒️ Estructura del repositorio


| Bloque                  | Contenido /    Función                                                        |
|--------------------------|-------------------------------------------------------------------------------------|
| Configuración inicial    | - Importación de librerías                                                          |
|                          | - Conexión a la base de datos                                                       |
|                          | - Creación de tablas (empleados, asistencia, cortes)                                |
| Interfaz gráfica         | - Creación del notebook con pestañas                                                |
|                          | - Pestaña de registro de asistencia                                                 |
|                          | - Pestaña de vista semanal                                                          |
|                          | - Pestaña de vista de reporte dinámico                                              |
| Funciones principales    | - cargar_vista_semana(): calcula rango lunes–domingo y muestra días trabajados       |
|                          | - cargar_vista_reporte(): genera reporte desde último corte hasta hoy y guarda TXT  |
|                          | - Funciones auxiliares para registrar entradas/salidas                              |
| Gestión de cortes        | - Tabla cortes para guardar fecha del último reporte                                |
|                          | - Inserción automática de nueva fecha de corte al generar reporte                   |
| Exportación de reportes  | - Generación de archivo TXT con nombre dinámico (reporte_fechaInicio_a_fechaFin.txt) |
|                          | - Carpeta reportes creada automáticamente si no existe                              |
| Interacción usuario      | - Botones en cada pestaña (Generar reporte, Cargar semana)                          |
|                          | - Tablas Treeview para mostrar resultados                                           |
|                          | - Labels para mostrar mensajes y resúmenes                                          |


## ​🗿​ Requisitos para ejecutar el programa


Programas / Entorno
Python  como VScode

SQLite 

Librerías de Python
tkinter para la interfaz gráfica 

sqlite3 para la conexión con la base de datos 

datetime para el manejo de fechas y cortes

os para gestión de carpetas y archivos 

