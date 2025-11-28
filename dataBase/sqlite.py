import sqlite3

# Conexión
conn = sqlite3.connect('dataBase/airbnb.db')

# Objeto cursor para query 
cursor = conn.cursor()

# tabla empleados
cursor.execute("""CREATE TABLE IF NOT EXISTS empleados (
               id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
               nombre TEXT NOT NULL,
               apellido TEXT NOT NULL,
               puesto TEXT NOT NULL,
               estado BOOLEAN NOT NULL,
               qr_codigo TEXT UNIQUE NOT NULL)
               """)

# tabla asistencia
cursor.execute("""CREATE TABLE IF NOT EXISTS asistencia (
               id_asistencia INTEGER PRIMARY KEY AUTOINCREMENT,
               id_empleado INTEGER NOT NULL,
               fecha DATE NOT NULL,
               hora_entrada TIME NULL,
               hora_salida TIME NULL,
               FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado))
               """)
# Modificar tu tabla cortes para que guarde los días por empleado
cursor.execute("""CREATE TABLE IF NOT EXISTS cortes (
                id_corte INTEGER PRIMARY KEY AUTOINCREMENT,
                id_empleado INTEGER,
                fecha_corte DATE NOT NULL,
                dias_trabajados INTEGER DEFAULT 0,
                FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado))
                """)
conn.commit()

# Función para insertar empleado
#def Insertar_empleado(empleado):
#    cursor.execute("INSERT INTO empleados VALUES (?,?,?,?,?)",
#                   (empleado.id_empleado, empleado.nombre, empleado.puesto, empleado.estado, empleado.codigo))
#   conn.commit()

# Cierre de conexión
conn.close()
