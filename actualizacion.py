import pandas as pd
import time
import smtplib
from datetime import datetime
import os
import email.message
from IPython.display import HTML

def ultima_actualizacion(ruta):
    try: 
        estado = os.stat(ruta)
        fecha = time.localtime(estado.st_mtime)
        fecha = datetime(fecha[0], fecha[1], fecha[2], fecha[3], fecha[4])
    except Exception as error:
        print("Verifique la ruta del archivo\n")
        print(f"EL error que se presento fue: {error}")
    else:
        return fecha

def envio_correo(origin_address, password, destination_address, message):
#
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(origin_address, password)
        server.sendmail(origin_address, destination_address, message)
        server.quit()

        
def envio_correo_df (subject, origin_address, password, destination_address, message, df):       
    
    content_table = df.to_html()
    msg = email.message.Message()
    msg['Subject'] = subject


    msg['From'] = origin_address
    msg['To'] = destination_address # puede ser uno solo o una lista con varios correos
    password = password
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(message + content_table)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    # Login Credentials for sending the mail
    s.login(msg['From'], password)

    s.sendmail(msg['From'], [msg['To']], msg.as_string())

archivo_csv = 'archivos.csv'
archivos = pd.read_csv(archivo_csv)
archivos_off = pd.DataFrame()
fecha_actual = datetime.now()

for index, x in archivos.iterrows():
    ruta = f"{x['ruta']}\\{x['archivo']}"
    fecha_actualizizacion = ultima_actualizacion(ruta)

    if (fecha_actual - fecha_actualizizacion).days > 0:
       
        archivos_off = archivos_off.append({'cliente': x['cod_cliente'], 
                                            'tipo_proceso': x['tipo_proceso'],'nombre_archivo': x['archivo'], 'ultima_modificacion': fecha_actualizizacion}, ignore_index = True, sort = True)

origin_address = EMAIL
password = PASSWORD
destination_address = 'judgomezlo@unal.edu.co' # tambien puede ser una lista con varios correos
subject = 'Ultima Prueba'
fecha_actual = datetime.strftime(fecha_actual,'%b %d, %Y')
if len(archivos_off) == 0:
    message = f"El dia {fecha_actual}, todos los archivos que se encuentra en {archivo_csv} fueron actualizados correctamente"
else:
    message = f"Los archivos que no se actualizaron correctamente hoy {fecha_actual}, segun la lista que se encuentra en {archivo_csv} fueron : \n\n\n\n"

envio_correo_df (subject, origin_address, password, destination_address, message, archivos_off)
