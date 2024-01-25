from con.connection import psql
from querys import *
from calculos import *

try:
    conexion = psql()
    if conexion: # Verificar si la conexión está abierta
        print("Conexión exitosa a la base de datos PostgreSQL")
        
        #^ Creacion e insercion de Instrumento y Path instrumento inexistentes
        #^ se debe agregar Path grupo a mano en la tabla rp_ponderaciones_path
        instrumentos_mt5 = func_sel_mt5_instrumento_path(conexion) #& Obtiene todos los instrumentos y su Path
        instrumentos_path = func_sel_path_instrumento(conexion) #& Obtiene todos los instrumentos de la tabla rp_ponderaciones_path
        sin_path_grupo = func_path_grupo_vacio(instrumentos_mt5, instrumentos_path) #& Se debe llenar el grupo a mano en la tabla rp_ponderaciones_path
        func_ins_path(conexion, sin_path_grupo) #& Inserta el instrumento y el Path Instrumento en la tabla, se debe agregar a mano el Path Grupo
        
        #^ Crea los instrumentos faltantes y terminan en una variable llamada nuevas ponderaciones
        instrumentos_faltantes = func_sel_instrumentos_faltantes(conexion)
        monto_moneda_a_usd = func_sel_monto_moneda_usd(conexion)
        ponderacion_base = func_sel_generacion_data_base_mt5(conexion,instrumentos_faltantes)
        nuevas_ponderaciones = func_ponderaciones_campos_no_calculados(ponderacion_base)
        nuevas_ponderaciones = func_ponderaciones_campos_calculados(nuevas_ponderaciones,instrumentos_faltantes,monto_moneda_a_usd)
        
        #^ Crea los agrupacion en base a la union de los grupos reales y los grupos de simbolos
        grupos_reales = func_sel_grupos_reales(conexion)
        grupos_simbolos = func_sel_grupos_simbolos(conexion)
        grupos = func_grupos_y_simbolos(grupos_reales,grupos_simbolos)
        agrupacion = func_agrupacion_categoria(grupos)
        
        #^ Junta las Nuevas Ponderaciones con la Agrupacion dejando un Codigo unico
        nuevas_ponderaciones = func_agregar_spread_ponderaciones_premium_vip(nuevas_ponderaciones, agrupacion)

        #^ Verifica los instrumentos que ya existen en la BDD
        viejas_ponderaciones = func_sel_instrumentos_old(conexion, instrumentos_faltantes)
        insert, update, no_update = func_actualiza_ponderaciones(viejas_ponderaciones,nuevas_ponderaciones)
        print(f"\n\nNuevo ({len(insert)}): {[symbol for symbol in insert]}\n\nActualizado ({len(update)}): {[symbol for symbol in update]}\n\nNo Actualizado ({len(no_update)}): {[symbol for symbol in no_update]}")
        
        #^ Inserta (tabla historica y update) y Actualiza (update) en la Base de Datos
        func_ins_datos_ponderados_historicos(conexion, nuevas_ponderaciones) #& para la tabla rp_ponderacionxsymbol_python_historical
        func_ins_datos_ponderados(conexion, insert) #& para la tabla rp_ponderacionxsymbol_python_update
        func_upd_datos_ponderados(conexion,update) #& para la tabla rp_ponderacionxsymbol_python_update
except psql().Error as e:
    print("Error al conectar a la base de datos PostgreSQL: {}".format(e))
finally:
    conexion.close() # Pa que quede bien cerra la wea xD
print("Conexion cerrada.")