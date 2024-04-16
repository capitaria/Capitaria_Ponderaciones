from con.connection import psql
from querys import *
from calculos import *
from datetime import datetime # para trabajar con fechas
from time import time as crono # cronometro

# fecha_consultada = datetime.now().date()
fecha_consultada = '2024-03-25' # Comentar para tomar fecha now().date()
fecha_consultada = datetime.strptime(fecha_consultada, "%Y-%m-%d").date() # Comentar para tomar fecha now().date()
nombre_dia_semana = fecha_consultada.strftime("%A")
numero_dia_semana  = fecha_consultada.weekday() + 1 # 1 para Lunes / 7 para Domingo

if numero_dia_semana <= 5:
    try:
        conexion = psql()
        if conexion: # Verificar si la conexión está abierta
            inicio = crono()
            print("Conexión exitosa a la base de datos PostgreSQL")
            
            fecha_prox_mes_fiscal_correcta = func_mes_fiscal(fecha_consultada)
            
            
            #^ Insercion de "Instrumento" y Actualizacion de "Path Instrumento"
            instrumentos_mt5 = func_sel_mt5_instrumento_path(conexion)
            instrumentos_path = func_sel_path_instrumento(conexion)
            insert_path, update_path, no_update_path = func_actualiza_path_instrumentos(instrumentos_mt5,instrumentos_path)
            #func_ins_instrumento_path(conexion, insert_path) #* insert PSQL
            #func_upd_path_instrumento(conexion, update_path) #* update PSQL
                    
            #^ Agrega y/o Actualiza el Path Grupo de forma automatica
            paths_grupos_faltantes = func_sel_path_grupo_faltante(conexion,update_path)
            paths_grupos = func_sel_grupos_existentes(conexion)
            llenado_path_grupo = func_llenado_path_grupo(paths_grupos_faltantes, paths_grupos)
            #func_upd_path_grupo(conexion,llenado_path_grupo) #* update PSQL
            
            #^ Crea los instrumentos faltantes
            instrumentos_faltantes = func_sel_instrumentos_faltantes(conexion,fecha_consultada) #& modificar instrumentos
            monto_moneda_a_usd = func_sel_monto_moneda_usd(conexion, fecha_consultada)
            ponderacion_base = func_sel_generacion_data_base_mt5(conexion,instrumentos_faltantes)
            nuevas_ponderaciones = func_ponderaciones_campos_no_calculados(ponderacion_base)
            nuevas_ponderaciones = func_ponderaciones_campos_calculados(nuevas_ponderaciones,instrumentos_faltantes,monto_moneda_a_usd)
            
            #^ Crea las agrupaciones en base a la union de los grupos reales y los grupos de simbolos
            grupos_reales = func_sel_grupos_reales(conexion) #& modificar grupos
            grupos_simbolos = func_sel_grupos_simbolos(conexion) #& modificar grupos
            grupos = func_grupos_y_simbolos(grupos_reales,grupos_simbolos)
            agrupacion = func_agrupacion_categoria(grupos)   

            #^ Junta las Nuevas Ponderaciones con la Agrupacion dejando un Codigo unico
            nuevas_ponderaciones = func_agregar_spread_ponderaciones_premium_vip(nuevas_ponderaciones, agrupacion)
            
            #^ Inserta (tabla historica) y Actualiza (tabla mensual) en la Base de Datos
            #func_ins_datos_ponderados_historicos(conexion, nuevas_ponderaciones) #* insert PSQL
            if fecha_consultada == fecha_prox_mes_fiscal_correcta: #todo Se actualiza los cierres de mes
                func_ins_datos_ponderados(conexion, nuevas_ponderaciones)
                #// viejas_ponderaciones = func_sel_instrumentos_old_historical(conexion, instrumentos_faltantes, fecha_consultada) #! BORRAR 1
                #// insert_instrumento, update_instrumento, no_update_instrumento = func_actualiza_ponderaciones(viejas_ponderaciones,nuevas_ponderaciones) #! BORRAR 2
                #// func_sel_instrumentos_old_update(conexion,instrumentos_faltantes) #! BORRAR 3
                #// func_ins_datos_ponderados(conexion, insert_instrumento) #! BORRAR 4
                #// func_upd_datos_ponderados(conexion,update_instrumento) #! BORRAR 5
                            
            #^ INFO
            fin = crono()
            print(f'\n************************************************\n{"INFO ADICIONAL"}\n************************************************')
            print(f"Tiempo Estimado: {tiempo_exacto(fin-inicio)}")
            print(f"Fecha Consultada: {fecha_consultada}")
            print(f"Fecha Proximo Mes Fiscal: {fecha_prox_mes_fiscal_correcta}")
            print(f'************************************************')
            
    except psql().Error as e:
        print("Error al conectar a la base de datos PostgreSQL: {}".format(e))
    finally:
        conexion.close() # Pa que quede bien cerra la wea xD
    print("Conexion cerrada.")
else:
    print(f"Día {nombre_dia_semana} {numero_dia_semana}")