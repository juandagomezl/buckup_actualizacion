import shutil
import boto3
import pandas as pd
from datetime import datetime
import os



def compress (new_path, extension, path):
    
    shutil.get_archive_formats()
    shutil.make_archive(new_path, extension, path)

def connection_s3(region, acces_key, secret_access_key):
    
    s3 = boto3.client('s3',
        region_name = region,
        aws_access_key_id = acces_key,
        aws_secret_access_key = secret_access_key
    )
    return s3

def backup_in_s3 (connection, path, bucket_name, file_name):
    
    connection.upload_file(
        Filename = path,
        Bucket= bucket_name,
        Key= file_name
    )  


def backup (connection, path_csv):
    print(1)
    now = datetime.now().strftime('%Y%m%d')
    paths = pd.read_csv(path_csv)
    

    for index, files in paths.iterrows():
        file = f"{files['path_file']}\\{files['name_file']}"
        fecha_actual = f"{now}\\{files['name_file']}"
        print(2)
        print(file)
        print(fecha_actual)
        shutil.copytree(file, fecha_actual)
        fecha_actual = now
        
        
    compress (f"{now}", "zip", f"{now}")
    backup_in_s3 (connection, f"{now}.zip", "coosalud-direktio", f"backups/{now}.zip")
    
    os.remove(f"{now}.zip")
    shutil.rmtree(f"{now}")
    
path_csv = 'prueba_buckup.csv'
s3 = connection_s3('us-east-1', AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY_ID)


try: 

    backup(s3, path_csv)  

except FileNotFoundError as error:
    mensaje = "El path o el file_name no se encontraron o se encuentran mal especificados"
    print(f"Error -> {error}. {mensaje}")

else:

    print("buckup exitoso")
