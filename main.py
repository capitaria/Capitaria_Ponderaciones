from con.connection import psql
from querys import *
from calculos import *
from datetime import datetime # para trabajar con fechas
from time import time as crono # cronometro

fecha_consultada = datetime.now().date()

try:
    conexion = psql()
    if conexion: # Verificar si la conexión está abierta
        inicio = crono()
        print("Conexión exitosa a la base de datos PostgreSQL")
        
        # #^ Insercion de "Instrumento" y Actualizacion de "Path Instrumento"
        # instrumentos_mt5 = func_sel_mt5_instrumento_path(conexion) #* SELECT
        # instrumentos_path = func_sel_path_instrumento(conexion) #* SELECT
        # insert_path, update_path, no_update_path = func_actualiza_path_instrumentos(instrumentos_mt5,instrumentos_path)
        # #// print(f"\nInsert ({len(insert_path)}): {[x[0] for x in insert_path]}")
        # #// print(f"\nUpdate ({len(update_path)}): {[x[0] for x in update_path]}")
        # #// print(f"\nNo Update ({len(no_update_path)})\n")
        # func_ins_instrumento_path(conexion, insert_path) #! INSERT
        # func_upd_path_instrumento(conexion, update_path) #! UPDATE
        
        # #^ Agrega y/o Actualiza el Path Grupo de forma automatica
        # paths_grupos_faltantes = func_sel_path_grupo_faltante(conexion,update_path) #* SELECT
        # paths_grupos = func_sel_grupos_existentes(conexion) #* SELECT
        # llenado_path_grupo = func_llenado_path_grupo(paths_grupos_faltantes, paths_grupos)
        # func_ins_upd_path_grupo(conexion,llenado_path_grupo) #! INSERT

        #^ Crea los instrumentos faltantes
        instrumentos_faltantes = func_sel_instrumentos_faltantes(conexion) #* SELECT - FECHA (Mod)
        monto_moneda_a_usd = func_sel_monto_moneda_usd(conexion) #* SELECT (Mod)
        ponderacion_base = func_sel_generacion_data_base_mt5(conexion,instrumentos_faltantes) #* SELECT (Mod)
        nuevas_ponderaciones = func_ponderaciones_campos_no_calculados(ponderacion_base)
        nuevas_ponderaciones = func_ponderaciones_campos_calculados(nuevas_ponderaciones,instrumentos_faltantes,monto_moneda_a_usd)
        
        #^ Crea las agrupaciones en base a la union de los grupos reales y los grupos de simbolos
        grupos_reales = func_sel_grupos_reales(conexion) #* SELECT (Mod)
        grupos_simbolos = func_sel_grupos_simbolos(conexion) #* SELECT (Mod)
        print(grupos_simbolos)
        breakpoint()
        grupos = func_grupos_y_simbolos(grupos_reales,grupos_simbolos)
        agrupacion = func_agrupacion_categoria(grupos)
        
        #^ Junta las Nuevas Ponderaciones con la Agrupacion dejando un Codigo unico
        #print('\nnuevas ponderaciones: ',nuevas_ponderaciones,'\n\nagrupacion: ',agrupacion,'\n')
        nuevas_ponderaciones = func_agregar_spread_ponderaciones_premium_vip(nuevas_ponderaciones, agrupacion) #todo - Revision
        
        #^ Verifica los instrumentos que ya existen en la BDD
        viejas_ponderaciones = func_sel_instrumentos_old_historical(conexion, instrumentos_faltantes)
        insert_instrumento, update_instrumento, no_update_instrumento = func_actualiza_ponderaciones(viejas_ponderaciones,nuevas_ponderaciones)
        print(f"\nInsert ({len(insert_instrumento)}) // Update ({len(update_instrumento)}) // No Update ({len(no_update_instrumento)})\n")        
        
        #^ Inserta (tabla historica y update) y Actualiza (update) en la Base de Datos
        #func_ins_datos_ponderados_historicos(conexion, nuevas_ponderaciones) #! INSERT
        fecha_prox_mes_fiscal_exacta, fecha_prox_mes_fiscal_correcta = func_mes_fiscal(fecha_consultada)
        # if fecha_consultada == fecha_prox_mes_fiscal_correcta: #todo Se actualiza los cierres de mes
        #     #func_sel_instrumentos_old_update(conexion,instrumentos_faltantes) #& REVISAR EL 23
        #     func_ins_datos_ponderados(conexion, insert_instrumento) 
        #     func_upd_datos_ponderados(conexion,update_instrumento)
                        
        #^ INFO
        fin = crono()
        print(f'\n******\n{"INFO ADICIONAL"}\n******\n')
        print(f"Fecha Consultada: {fecha_consultada}")
        print(f"Tiempo Estimado: {tiempo_exacto(fin-inicio)}")
        # print(f"Path Nuevos: {len(insert_path)}")
        # print(f"Path Actualizados: {len(update_path)}")
        # print(f"Path No Actualizados: {len(no_update_path)}")
        print(f"Instrumentos Nuevos: {len(insert_instrumento)}")
        print(f"Instrumentos Actualizados: {len(update_instrumento)}")
        print(f"Instrumentos No Actualizados: {len(no_update_instrumento)}")
        #// print(f"Fecha Proximo Mes Fiscal Exacta: \t\t{fecha_prox_mes_fiscal_exacta}")   
        print(f"Fecha Proximo Mes Fiscal: {fecha_prox_mes_fiscal_correcta}")
        
except psql().Error as e:
    print("Error al conectar a la base de datos PostgreSQL: {}".format(e))
finally:
    conexion.close() # Pa que quede bien cerra la wea xD
print("Conexion cerrada.")