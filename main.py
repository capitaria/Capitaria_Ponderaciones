from con.connection import psql
from querys import *
from calculos import *

#calculo_ponderaciones = list()

try:
    conexion = psql()
    if conexion: # Verificar si la conexión está abierta
        print("Conexión exitosa a la base de datos PostgreSQL")
        ponderacion_base = generacion_data_base_mt5(conexion)
        ponderacion_calculada = calculo_ponderaciones(ponderacion_base)
        print(f'\nPONDERACION BASE\n******\n{ponderacion_base}\n******\n\n')
        print(f'\nPONDERACION CALCULADA\n******\n{ponderacion_calculada}\n******\n\n')
except psql().Error as e:
    print("Error al conectar a la base de datos PostgreSQL: {}".format(e))
finally:
    conexion.close() # Pa que quede bien cerra la wea xD
    print("Conexion cerrada.")