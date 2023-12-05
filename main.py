from con.connection import psql
from querys import *
from calculos import *

try:
    conexion = psql()
    if conexion: # Verificar si la conexión está abierta
        print("Conexión exitosa a la base de datos PostgreSQL")
        instrumentos_faltantes = func_sel_instrumentos_faltantes(conexion)
        calculo_a_usd = func_sel_monto_moneda_usd(conexion)
        ponderacion_base = func_sel_generacion_data_base_mt5(conexion,instrumentos_faltantes)
        campos_rp_ponderacionxsymbol_python = func_sel_campos_rp_ponderacionxsymbol_python(conexion)
        #! eliminar - precios = func_sel_obtener_precio(conexion, instrumentos_faltantes)
        nuevas_ponderaciones = func_ponderaciones_campos_no_calculados(ponderacion_base)
        print(nuevas_ponderaciones)
        # nuevas_ponderaciones = func_ponderaciones_campos_calculados(nuevas_ponderaciones,precios,calculo_a_usd)
        # func_ins_datos_ponderados(conexion, campos_rp_ponderacionxsymbol_python, nuevas_ponderaciones)
except psql().Error as e:
    print("Error al conectar a la base de datos PostgreSQL: {}".format(e))
finally:
    conexion.close() # Pa que quede bien cerra la wea xD
    print("Conexion cerrada.")