import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import qrcode
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
from datetime import date, timedelta
from datetime import datetime, timedelta
from datetime import datetime, timedelta, date



# se hace la coneccion a la base de datos.......................
conn = sqlite3.connect("dataBase/airbnb.db")
cursor = conn.cursor()

# se incializa la ventana principal.......................................................
ventana = tk.Tk() #crea una ventana la cual es la pricipal en la aplicacion
ventana.title("Sistema de Control de Empleados")

#se crea la parte de pestañas dentro de la variable ventana (es la ventana principal)
notebook = ttk.Notebook(ventana)
notebook.pack(expand=True, fill="both")

# primera pestañas de trabajadores (estado de trabajadores)..................................................................

frame_estado = ttk.Frame(notebook)#frame que nuestra el estado de los trabajadores
notebook.add(frame_estado, text="Estado trabajadores")

#configuracion de tabla para ver el estado de los trabajadores
tabla_estado = ttk.Treeview(frame_estado, columns=("ID","Nombre completo","Estado"), show="headings")
tabla_estado.heading("ID", text="ID")
tabla_estado.heading("Nombre completo", text="Nombre completo")
tabla_estado.heading("Estado", text="Estado")
tabla_estado.pack(expand=True, fill="both")

"""carga y muestra en la tabla el estado actual de los trabjadores y jala datos de la bd 
y limpia los datos """

def cargar_estado():
    tabla_estado.delete(*tabla_estado.get_children()) #limpia la tabla antes de cargar los nuevos datos y asi no se duplican  los trbajadores
    cursor.execute("SELECT id_empleado, nombre, apellido, estado FROM empleados")#consulta los empleados desde la db
    #inserta el noembre, apellido y estado en la tabla
    for id_emp, nombre, apellido, estado in cursor.fetchall():
        nombre_completo = f"{nombre} {apellido}"
        estado_txt = "Activo" if estado else "Ausente"
        tabla_estado.insert("", "end", values=(id_emp, nombre_completo, estado_txt))

#para cargar el estado al incializar el programa
cargar_estado()

# segunda pestaña de trabajadores(gestion de empleados)................
#frame par agregar, buscar o eliminar empleados
frame_agregar = ttk.Frame(notebook)
notebook.add(frame_agregar, text="Gestion de Empleados")


#creacion de etiquetas labels
tk.Label(frame_agregar, text="Nombre").grid(row=0, column=0, sticky="w")#w de west(izquierda)
tk.Label(frame_agregar, text="Apellido").grid(row=1, column=0, sticky="w")
tk.Label(frame_agregar, text="Puesto").grid(row=2, column=0, sticky="w")

#creacion de campos para escribir loa datos ingresador por el usuario
nombre_entry = tk.Entry(frame_agregar)
apellido_entry = tk.Entry(frame_agregar)
puesto_entry = tk.Entry(frame_agregar)

nombre_entry.grid(row=0, column=1, sticky="ew")#para que se estire hacia la izquierda y derecha
apellido_entry.grid(row=1, column=1, sticky="ew")
puesto_entry.grid(row=2, column=1, sticky="ew")


 #laber para mistar el codigogenerado
qr_label = tk.Label(frame_agregar)
qr_label.grid(row=4, column=0, columnspan=2)


# Función para generar credencial en formato de imagen y pdf
def generar_credencial(nombre, apellido, puesto, emp_id, qr_img):
    try:
        # configurasion de tamaño de la tarjeta segun el estandar
        ancho_tarjeta = 1013  
        alto_tarjeta = 638    
        
        # creamod la foto con el mañaño que pusimos 
        credencial = Image.new("RGB", (ancho_tarjeta, alto_tarjeta), "#FFFDD0")  # lo hacemos de color crema
        draw = ImageDraw.Draw(credencial)

        # le ponemos in lmite para recorte punteado
        dash_length = 20
        space_length = 10

        #hacemos las lineas de color rojo
        # linea de arriba
        for x in range(0, ancho_tarjeta, dash_length + space_length):
            draw.line([(x, 5), (x + dash_length, 5)], fill="red", width=3)
        
        # linea de abajo
        for x in range(0, ancho_tarjeta, dash_length + space_length):
            draw.line([(x, alto_tarjeta-5), (x + dash_length, alto_tarjeta-5)], fill="red", width=3)
        
        # linea de la izquierda
        for y in range(0, alto_tarjeta, dash_length + space_length):
            draw.line([(5, y), (5, y + dash_length)], fill="red", width=3)
        
        # linea de la derecha
        for y in range(0, alto_tarjeta, dash_length + space_length):
            draw.line([(ancho_tarjeta-5, y), (ancho_tarjeta-5, y + dash_length)], fill="red", width=3)

        # hacemos un cuadrado para donde ira la foto del empleado
        foto_x1, foto_y1 = 80, 80
        foto_x2, foto_y2 = 380, 380
        draw.rectangle([foto_x1, foto_y1, foto_x2, foto_y2], outline="black", width=4)
        draw.text((foto_x1 + 100, foto_y1 + 120), "FOTO", fill="gray", font=ImageFont.load_default())

        #le damos el tamalo del qr y lo insertamos
        qr_size = 400  #le damos el tamañaño
        qr_img_resized = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
        credencial.paste(qr_img_resized, (550, 100))

        # fuentes para el texto de la imagen con un try para que si no encuentra la fuente ponga el deafult
        try:
            font_titulo = ImageFont.truetype("arial.ttf", 28)
            font_normal = ImageFont.truetype("arial.ttf", 24)
            font_pequeno = ImageFont.truetype("arial.ttf", 20)
        except:
            font_titulo = ImageFont.load_default()
            font_normal = ImageFont.load_default()
            font_pequeno = ImageFont.load_default()

        #le damos lugar y posicion a la info del empleado
        info_x = 80
        info_y = 420
        
        #esto es para poner la inFORMACION DEL EMPLEADO EN LA CREDENCIAL
        draw.text((info_x, info_y), f"ID: EMP{emp_id:04d}", font=font_normal, fill="black")
        draw.text((info_x, info_y + 45), f"Nombre: {nombre} {apellido}", font=font_normal, fill="black")
        draw.text((info_x, info_y + 90), f"Puesto: {puesto}", font=font_normal, fill="black")
        
        

        #guarda la credencial en ambos formatos
        credencial_png = f"credenciales/credencial_{emp_id}.png"
        credencial.save(credencial_png, "PNG", dpi=(300, 300))


        credencial_pdf = f"credenciales/credencial_{emp_id}.pdf"
        credencial.save(credencial_pdf, "PDF", resolution=300)

        print(f"Credencial guardada: {credencial_png} y {credencial_pdf}")
        return True
    except Exception as e:
        print(f"Error al generar credencial: {e}")
        return False

#funcion para agreagar un empleado..................................
"""hace el proceso de agregar un nuevo empleado y esto fvalida y genera el qr junto con la cracion de la credencial 
junto con lo que asignadmos arriba"""
def agregar_empleado():
    try:
        #recibe u valida los datos ingresados
        nombre = nombre_entry.get().strip()
        apellido = apellido_entry.get().strip()
        puesto = puesto_entry.get().strip()
        
        #esto valida los campos para que se ingrsen si o si y no queden vacios por que puede dar error despues
        if not nombre or not apellido or not puesto:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return False

        #genera el codigo  qr juntando las primerad letras de los nombres y epellidos
        qr_codigo = f"{nombre[:3]}{apellido[:3]}".upper().strip()

        #inserta el nuevo empleado en la base de datos
        cursor.execute("""
            INSERT INTO empleados (nombre, apellido, puesto, estado, qr_codigo) 
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, apellido, puesto, True, qr_codigo))
        conn.commit()
        
        #obtiene el id asigando automaticamente
        emp_id = cursor.lastrowid
        print(f"Empleado agregado con ID: {emp_id}")

        #genera el codigo qr
        qr_data = f"{nombre[:3]}{apellido[:3]}".upper() #esrructura del nomvre 
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").resize((100, 100))
        
        #pone el qr en el el cuadro que aginamos arriba en la intrfaz
        qr_img_tk = ImageTk.PhotoImage(qr_img)
        qr_label.config(image=qr_img_tk, text="")
        qr_label.image = qr_img_tk

        #aqui se genera la credencial 
        if generar_credencial(nombre, apellido, puesto, emp_id, qr_img):
            messagebox.showinfo("Éxito", 
                f"Empleado agregado exitosamente!\n\n"
                f"Nombre: {nombre} {apellido}\n"
                f"Puesto: {puesto}\n"
                f"ID: {emp_id}\n"
                f"QR: {qr_data}\n\n"
                f"Credencial guardada en: credenciales/credencial_{emp_id}.png")# lo guardamos en una carpeta para llevar un orden 
            
           #por si algo no sale mal ponermos un mensaje de que hubo un error al general la credencial
        else:
            messagebox.showwarning("Advertencia", 
                f"Empleado agregado pero hubo problemas al generar la credencial.\n"
                f"ID: {emp_id}")

        #esto hace que a la hora de hacer el registro limpie los campos en automatico
        nombre_entry.delete(0, tk.END)
        apellido_entry.delete(0, tk.END)
        puesto_entry.delete(0, tk.END)
        
        #aqui es para actualizar la tabla de estado y que no estemos abriendo y cerrando el sistema
        cargar_estado()
        return True

    except Exception as e:
        messagebox.showerror("Error", f"Error al agregar empleado: {str(e)}")
        return False

#boton para ejecutar el registro de empleados
btn_agregar = tk.Button(frame_agregar, text="Agregar empleado", command=agregar_empleado, 
                       bg="green", fg="white", font=("Arial", 10, "bold"))
btn_agregar.grid(row=3, column=0, columnspan=2, pady=10, padx=5, sticky="ew")


#parte de busacr y eliminar ............................
#configuraxzion de la intefaz para buscar los empleados
tk.Label(frame_agregar, text="Buscar por nombre o apellido").grid(row=6, column=0, sticky="w", pady=(10,2))
busqueda_entry = tk.Entry(frame_agregar)
busqueda_entry.grid(row=6, column=1, sticky="ew")

tabla_busqueda = ttk.Treeview(frame_agregar, columns=("ID","Nombre completo","Puesto"), show="headings")
tabla_busqueda.heading("ID", text="ID")
tabla_busqueda.heading("Nombre completo", text="Nombre completo")
tabla_busqueda.heading("Puesto", text="Puesto")
tabla_busqueda.grid(row=7, column=0, columnspan=2, sticky="nsew", pady=(5,5))

def buscar_empleado():
    """esta funcion es para buscvar los empleados en la db por nombre o apellido 
    y mustra los resultados en la tabl"""
    termino = busqueda_entry.get().strip()
    #elimina los resultados buscados anteriores asi evitas que aparezaca la tabla llene de usuarios buscados antes
    tabla_busqueda.delete(*tabla_busqueda.get_children())
    #aqui busca los empleados que hayamos buscado meidante lo que pusimos
    cursor.execute("""
        SELECT id_empleado, nombre, apellido, puesto
        FROM empleados
        WHERE nombre LIKE ? OR apellido LIKE ?
    """, (f"%{termino}%", f"%{termino}%"))

    #muestra el resultado en la tabla
    for id_emp, nombre, apellido, puesto in cursor.fetchall():
        nombre_completo = f"{nombre} {apellido}"
        tabla_busqueda.insert("", "end", values=(id_emp, nombre_completo, puesto))

        busqueda_entry.delete(0, tk.END)
#boton para hacer las busqueda
tk.Button(frame_agregar, text="Buscar", command=buscar_empleado).grid(row=8, column=0, sticky="ew", pady=(5,5))

def eliminar_empleado():
    #esto verifica ue se haya seleccionado un empleado en la taba
    seleccionado = tabla_busqueda.selection()
    if not seleccionado:
        messagebox.showwarning("Porfavor", "Selecciona un empleado.")
        return
    #obtiene los datos del empleado seleccionado
    valores = tabla_busqueda.item(seleccionado[0], "values")
    id_empleado = valores[0]
    #pregunta si en verdad quiere eliminar los datos
    if not messagebox.askyesno("Confirmar", f"¿Desea eliminar al empleado ID {id_empleado}?"):
        return
    #se jecuta la eliminacion del trabajdaro enla base de datps
    cursor.execute("DELETE FROM empleados WHERE id_empleado = ?", (id_empleado,))
    conn.commit()
    #borra al usuario eliminado de la tabla
    tabla_busqueda.delete(seleccionado[0])
    cargar_estado()
    messagebox.showinfo("ÉXITO", f"Enpleado con ID {id_empleado} eliminado.")
#es el boton para ejevutar eliminar empleado
tk.Button(frame_agregar, text="Eliminar empleado", command=eliminar_empleado).grid(row=8, column=1, sticky="ew", pady=(5,5))

# tercera pertaña (ver dias trabajados)...........................................

# Aquí se arma el frame para mostrar los días trabajados desde el último corte
frame_vista = ttk.Frame(notebook)
notebook.add(frame_vista, text="Vista de reporte")

# Se configura la tabla para mostrar nombre y días trabajados
tabla_vista = ttk.Treeview(frame_vista, columns=("Nombre","Días trabajados"), show="headings")
tabla_vista.heading("Nombre", text="Nombre")
tabla_vista.heading("Días trabajados", text="Días trabajados")
tabla_vista.pack(expand=True, fill="both")

# Se agrega un label para mostrar el resumen en texto
lbl_status = tk.Label(frame_vista, text="", justify="left", font=("Arial", 12), fg="black")
lbl_status.pack(pady=10)

def cargar_vista_reporte():
    """
    Esto genera un reporte desde la última fecha de corte hasta el momento que aplasto el botón.
    Me muestra los días trabajados por cada empleado y guarda el reporte en un archivo TXT.
    """

    # Limpio la tabla antes de cargar nuevos datos
    tabla_vista.delete(*tabla_vista.get_children())

    # Obtengo la última fecha de corte registrada
    cursor.execute("SELECT MAX(fecha_corte) FROM cortes")
    ultima_fecha = cursor.fetchone()[0]

    # Si no hay cortes previos, uso una fecha antigua para que agarre todo
    if ultima_fecha is None:
        ultima_fecha = "2000-01-01"

    # Tomo la fecha actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    # Hago la consulta para contar los días trabajados desde el último corte
    cursor.execute("""
        SELECT e.nombre || ' ' || e.apellido AS nombre_completo,
               COUNT(DISTINCT a.fecha) AS dias_trabajados
        FROM asistencia a
        JOIN empleados e ON a.id_empleado = e.id_empleado
        WHERE a.fecha > ? AND a.fecha <= ?
          AND a.hora_entrada IS NOT NULL
          AND a.hora_salida IS NOT NULL
        GROUP BY e.id_empleado
    """, (ultima_fecha, fecha_actual))

    resultados = cursor.fetchall()

    # Armo el texto del reporte
    reporte = f"Reporte desde {ultima_fecha} hasta {fecha_actual}:\n"

    # Si hay resultados, los meto en la tabla y en el texto
    if resultados:
        for nombre_completo, dias in resultados:
            reporte += f"{nombre_completo}: {dias} días trabajados\n"
            tabla_vista.insert("", "end", values=(nombre_completo, f"{dias} días"))
    else:
        # Si no hay datos, muestro eso
        reporte += "No hay registros en este periodo.\n"
        tabla_vista.insert("", "end", values=("Sin datos", "0 días"))

    # Muestro el reporte en el label
    lbl_status.config(text=reporte)

    # Guardo el archivo en la carpeta "reportes"
    import os
    os.makedirs("reportes", exist_ok=True)  # Creo la carpeta si no existe
    nombre_archivo = os.path.join("reportes", f"reporte_{ultima_fecha}_a_{fecha_actual}.txt")
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(reporte)

    # Registro la nueva fecha de corte (esto reinicia el contador)
    cursor.execute("INSERT INTO cortes (fecha_corte) VALUES (?)", (fecha_actual,))
    conn.commit()

    print(f"✅ Reporte guardado en {nombre_archivo}")

# Botón para generar el reporte, solo aparece en esta pestaña
btn_reporte = tk.Button(frame_vista, text="Generar reporte", command=cargar_vista_reporte)
btn_reporte.pack(pady=10)

# Cargar datos al iniciar (opcional, si quieres que se vea algo al abrir)
cargar_vista_reporte()


"""def cargar_vista_semana():
   
    tabla_vista.delete(*tabla_vista.get_children())

    #calcual semana actual
    hoy = date.today()
    inicio_semana = hoy - timedelta(days=hoy.weekday())   # lunes
    fin_semana = inicio_semana + timedelta(days=6)        # domingo"""

    #cursor.execute("""
     #   SELECT e.nombre || ' ' || e.apellido AS nombre_completo,
      #         COUNT(DISTINCT a.fecha) AS dias_trabajados
       # FROM asistencia a
        #JOIN empleados e ON a.id_empleado = e.id_empleado
        #WHERE a.fecha BETWEEN ? AND ?
        #  AND a.hora_entrada IS NOT NULL
         # AND a.hora_salida IS NOT NULL
        #GROUP BY e.id_empleado
    #""", (inicio_semana, fin_semana))

#    for nombre_completo, dias in cursor.fetchall():
 #       tabla_vista.insert("", "end", values=(nombre_completo, f"{dias} días"))



        
    
#cargar losdatos al iniciar
#cargar_vista_semana()



ventana.mainloop()
conn.close()
