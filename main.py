from con.connection import psql
from querys import *
from calculos import *

try:
    conexion = psql()
    if conexion: # Verificar si la conexión está abierta
        print("Conexión exitosa a la base de datos PostgreSQL")
        instrumentos_faltantes = func_sel_instrumentos_faltantes(conexion)
        #print(instrumentos_faltantes)
        calculo_a_usd = func_sel_monto_moneda_usd(conexion)
        ponderacion_base = func_sel_generacion_data_base_mt5(conexion,instrumentos_faltantes)
        nuevas_ponderaciones = func_ponderaciones_campos_no_calculados(ponderacion_base)
        nuevas_ponderaciones = func_ponderaciones_campos_calculados(nuevas_ponderaciones,instrumentos_faltantes,calculo_a_usd)
        viejas_ponderaciones = func_sel_instrumentos_old(conexion, instrumentos_faltantes)
        insert, update, no_update = func_actualiza_ponderaciones(viejas_ponderaciones,nuevas_ponderaciones)
        #print(f"\n\nINSERT: {insert}\n\nUPDATE: {update}\n\nNO UPDATE: {no_update}")
        func_ins_datos_ponderados_historicos(conexion, nuevas_ponderaciones) #& para la tabla rp_ponderacionxsymbol_python_historical
        func_ins_datos_ponderados(conexion, insert) #& para la tabla rp_ponderacionxsymbol_python_update
        func_upd_datos_ponderados(conexion, update) #& para la tabla rp_ponderacionxsymbol_python_update
except psql().Error as e:
    print("Error al conectar a la base de datos PostgreSQL: {}".format(e))
finally:
    conexion.close() # Pa que quede bien cerra la wea xD
print("Conexion cerrada.")