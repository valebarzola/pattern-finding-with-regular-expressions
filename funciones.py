import re
import pandas as pd
from datetime import datetime

def last_conection(data_filter):
    correcto = True
    seguir = True
    lista_columnas = []
    opciones_columnas = {
        '1': 'ID',
        '2': 'ID_Sesion',
        '3': 'ID_Conexión_unico',
        '4': 'Usuario',
        '5': 'IP_NAS_AP',
        '6': 'Inicio_de_Conexión_Dia',
        '7': 'Inicio_de_Conexión_Hora',
        '8': 'FIN_de_Conexión_Dia',
        '9': 'FIN_de_Conexión_Hora',
        '10': 'Session_Time',
        '11': 'MAC_AP',
        '12': 'MAC_Cliente',
    }
    while True:
        try:    
            # Solicitar al usuario que ingrese las fechas en formato español
            date_start_spanish = input('Ingrese la fecha de inicio de la búsqueda (DD-MM-YYYY): ')
            date_end_spanish = input('Ingrese la fecha de fin de la búsqueda (DD-MM-YYYY): ')
            
            # Convertir las fechas al formato inglés (YYYY-MM-DD) para manipulación interna
            date_start = datetime.strptime(date_start_spanish, '%d-%m-%Y').strftime('%Y-%m-%d')
            date_end = datetime.strptime(date_end_spanish, '%d-%m-%Y').strftime('%Y-%m-%d')
            patron_start = re.compile(r'^(?:19|20)\d\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])$')
            patron_end = re.compile(r'^(?:19|20)\d\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])$')
            if not (patron_start.match(date_start) and patron_end.match(date_end)):
                raise ValueError("Formato de fecha incorrecto.")
            if date_start > date_end:
                raise ValueError("La fecha de inicio no puede ser mayor que la fecha de fin.")
            print('Fecha de inicio y Fin correctas')
            break        
        except ValueError as e:
            print(f'Error: {e}')
            print('Por favor, intente de nuevo.')
    while correcto is True:
        rta2 = input(' Desea ver:\n\
                    1. los usuarios que han iniciado y finalizado su conexión en el intervalo de tiempo \n\
                    2.  Su conexión haya terminado en el intervalo de tiempo\n\
                    Respuesta : ')
        if rta2 == '1':
            correcto = False
            data_filter = data_filter[(data_filter['Inicio_de_Conexión_Dia'] >= date_start) & (data_filter['FIN_de_Conexión_Dia'] <= date_end)]
        elif rta2 == '2':
            correcto = False
            data_filter = data_filter[(data_filter['FIN_de_Conexión_Dia'] >= date_start) & (data_filter['FIN_de_Conexión_Dia'] <= date_end)]
        else:
            print(f'Opción {rta2} incorrecta, intente denuevo. ')
    while seguir:
        columnas_a_aniadir = input('''Seleccione los campos para la tabla separados por comas o 'E' para salir:\n
        1: ID
        2: ID_Sesion
        3: ID_Conexión_unico
        4: Usuario
        5: IP_NAS_AP
        6: Inicio_de_Conexión_Dia
        7: Inicio_de_Conexión_Hora
        8: FIN_de_Conexión_Dia
        9: FIN_de_Conexión_Hora
        10: Session_Time
        11: MAC_AP
        12: MAC_Cliente
        E: Salir\nRespuesta:  ''').split(',')
        for seleccion in columnas_a_aniadir:
            seleccion = seleccion.strip()  # Elimina espacios en blanco alrededor de la selección
            if seleccion.upper() == 'E':
                seguir = False
                break  # Sale del bucle si el usuario ingresa 'E'
            elif seleccion in opciones_columnas:
                lista_columnas.append(opciones_columnas[seleccion])
            else:
                print(f'Opción {seleccion} incorrecta, intente de nuevo.')
        if seguir:  # Si el usuario no ha elegido salir, procede a filtrar y exportar
            data_filter_finally = data_filter[lista_columnas]
            print('\n')
            print(data_filter_finally)
            print('\n')
            export(data_filter_finally)
            seguir=False
def export(data_filter_finally):
    rta = input('Desea exportar los datos? (Y/N):').lower()
    if rta == 'y':
        rta1 = input('Desea exportar los datos en formato CSV o Excel? (CSV/Excel):').lower()
        if rta1 == 'csv':
            nombre_archivo = input('Nombre del archvo: ')
            ruta_csv = f'./export/{nombre_archivo}.csv'
            data_filter_finally.to_csv(ruta_csv, index=False)
            print(f'Archivo guardado en {ruta_csv}')
        if rta1 == 'excel':
            nombre_archivo = input('Nombre del archvo: ')
            ruta_excel = f'./export/{nombre_archivo}.xlsx'
            data_filter_finally.to_excel(ruta_excel, index=False)
            print(f'Archivo guardado en {ruta_excel}')
    else:
        print('Gracias por usar el programa')


def guardar_DataFrame(dataframe):
    pd.set_option('display.width', None)  # Desactivar el ajuste automático del ancho
    pd.set_option('display.max_columns', None)  # Mostrar todas las columnas
    nombre_archivo = input('Nombre del archvo para los errores: ')
    ruta_csv = f'./export/{nombre_archivo}.csv'
    dataframe.to_csv(ruta_csv, index=False)
    print(f'Archivo guardado en {ruta_csv}')


expresiones_regulares = {
    'ID': r'^\d{6,7}$', 
    'ID_Sesion': r'^[A-F0-9]{8}-[A-F0-9]{8}$',
    'ID_Conexión_unico': r'^[a-f0-9]{16}$',
    'Usuario': r'^[a-zA-Z.-]{3,25}$',
    'IP_NAS_AP': r'^((?:192\.168\.247\.[0-9]{2})|(?:192\.168\.1\.20))$',
    'Inicio_de_Conexión_Dia': r'^(?:19|20)\d\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])$',
    'Inicio_de_Conexión_Hora': r'^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$',
    'FIN_de_Conexión_Dia': r'^(?:19|20)\d\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])$',
    'FIN_de_Conexión_Hora': r'^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$',
    'Session_Time': r'^\d+(\.\d+)?$',
    'MAC_AP':  r'^([0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2}:HCDD$',
    'MAC_Cliente': r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
}

