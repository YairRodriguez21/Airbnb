import sqlite3
import cv2
from pyzbar.pyzbar import decode
from datetime import datetime
from PIL import Image, ImageTk
import tkinter as tk

#conexcion a la base de datos
conn = sqlite3.connect('dataBase/airbnb.db') 
cursor = conn.cursor()

#funcion de registro......................................................
def registro(nombre, tipo, emp_id):
    hora = datetime.now().strftime("%H:%M:%S")
    fecha = datetime.now().strftime("%Y-%m-%d")

    if tipo == "Entrada":
        cursor.execute("INSERT INTO asistencia (id_empleado, fecha, hora_entrada) VALUES (?, ?, ?)",
                       (emp_id, fecha, hora))
    elif tipo == "Salida":
        cursor.execute("UPDATE asistencia SET hora_salida = ? WHERE id_empleado = ? AND fecha = ?",
                       (hora, emp_id, fecha))
    conn.commit()

    lbl_status.config(text=f"{tipo} registrada para {nombre} a las {hora}")

# Interfaz grafica..........................
#se inicializa laa interfaz
ventana = tk.Tk()
ventana.title("Airbnb San Cristóbal")
ventana.geometry("600x600")#tamaño

lbl_titulo = tk.Label(ventana, text="Airbnb San Cristóbal", font=("Arial Black", 20))
lbl_titulo.pack(pady=20)


def escanear_frame():
    """funcion de escanear el qr donde se abrira la camara y e ello
    se antendra a cada 30frames para no duplicar escaneo"""
    ret, frame = cap.read()
    if ret:
        #abre la camara en tkinder
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        lbl_cam.config(image=imgtk)
        lbl_cam.imgtk = imgtk

        #este for lee y desifra el qr
        for codigo in decode(frame):
            data = codigo.data.decode("utf-8").strip().upper()
            print("QR leído:", repr(data))  # es solo para veer en consolsa el codifo que lee

            #ya que se decodifica busca al empleado en base al y compara con la tabla qr_code
            cursor.execute("SELECT id_empleado, nombre, apellido FROM empleados WHERE TRIM(UPPER(qr_codigo)) = ?", (data,))
            resultado = cursor.fetchone()
            #sino lo encunetra aparece codigo no registrado
            if not resultado:
                lbl_status.config(text=f"Código no registrado")
                ventana.after(2000, lambda: lbl_status.config(text="")) #borra el msaje para que no aparezca en pantalla siempre
                break

            #este paso, si encuentra al usuario registra la entrada 
            emp_id, nombre, apellido = resultado
            nombre_completo = f"{nombre} {apellido}"
            fecha = datetime.now().strftime("%Y-%m-%d")
            hora = datetime.now().strftime("%H:%M:%S")

            #checa si tiene el registro del dia
            cursor.execute("SELECT id_asistencia, hora_entrada, hora_salida FROM asistencia WHERE id_empleado=? AND fecha=?",
                           (emp_id, fecha))
            registro_existente = cursor.fetchone()

            if registro_existente is None:
                #sino tiene registro del dia, ejecuta insert en la db en la tabla hora_entrada
                cursor.execute("""
                    INSERT INTO asistencia (id_empleado, fecha, hora_entrada)
                    VALUES (?, ?, ?)
                """, (emp_id, fecha, hora))
                conn.commit()
                lbl_status.config(text=f"Entrada registrada para {nombre_completo} a las {hora}")

            else:
                id_asistencia, hora_entrada, hora_salida = registro_existente

                    #si se escanea nuevamente y tiene un registro existente solo hace un ubdate en la hora de salida para
                    #no generar duplicaciones de dias
                cursor.execute("""
                    UPDATE asistencia
                    SET hora_salida = ?
                    WHERE id_asistencia = ?
                """, (hora, id_asistencia))
                conn.commit()
                #muestra mensaje de hora actualizada
                lbl_status.config(text=f"Salida actualizada para {nombre_completo} a las {hora}")
    #mantiene la ventana escaneando siempre cada 30 frames
    ventana.after(30, escanear_frame)


lbl_cam = tk.Label(ventana)
lbl_cam.pack()

lbl_status = tk.Label(ventana, text="", font=("Arial", 12))
lbl_status.pack(pady=20)

#enciende la camara
cap = cv2.VideoCapture(0)
ventana.after(100, escanear_frame)

ventana.mainloop()


cap.release()
cv2.destroyAllWindows()
conn.close()
