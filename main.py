from con.connection import psql
from querys import *
from calculos import *

#todo - Ya obtengo todos los datos necesarios, ahora falta insertar en la tabla reports.rp_ponderacionxsymbol_python

try:
    conexion = psql()
    if conexion: # Verificar si la conexión está abierta
        print("Conexión exitosa a la base de datos PostgreSQL")
        ponderacion_base = func_generacion_data_base_mt5(conexion)
        precios = func_obtener_precio(conexion)
        monto_moneda_a_usd = func_monto_moneda_usd(conexion)
        nuevas_ponderaciones = func_ponderaciones_campos_no_calculados(ponderacion_base)
        nuevas_ponderaciones = func_ponderaciones_campos_calculados(nuevas_ponderaciones,precios,monto_moneda_a_usd)
        print(nuevas_ponderaciones)
except psql().Error as e:
    print("Error al conectar a la base de datos PostgreSQL: {}".format(e))
finally:
    conexion.close() # Pa que quede bien cerra la wea xD
    print("Conexion cerrada.")