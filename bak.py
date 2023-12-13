# def func_upd_datos_ponderados(conexion, update):
#     # actualiza en reports.rp_ponderacionxsymbol_python_update
    
#     if len(update) >= 1:
#         new_ponderaciones_update = list()
#         for i in update:
#             datos = [
#                 i,
#                 update[i]['tipo_instrumento'],
#                 update[i]['tipo'],
#                 update[i]['precio'],
#                 update[i]['tamanio_contrato'],
#                 update[i]['moneda_calculo'],
#                 update[i]['monto_usd'],
#                 update[i]['spread_go'],
#                 update[i]['spread_pro'],
#                 update[i]['spread_vip'],
#                 update[i]['poderacion_go'],
#                 update[i]['poderacion_pro'],
#                 update[i]['poderacion_vip'],
#                 update[i]['path'],
#                 update[i]['fecha_insercion_precio'],
#                 update[i]['fecha_insercion_registro']
#             ]
#             new_ponderaciones_update.append(datos)
            
#         cursor = conexion.cursor()
    
#         rp_ponderacionxsymbol_python = (
#         f"""
#         update
#         reports.rp_ponderacionxsymbol_python_update
#         set
#             instrumento = %s,
#             tipo_instrumento = %s,
#             tipo = %s,
#             precio = %s,
#             tamano_contrato = %s,
#             moneda_calculo = '%s',
#             monto_usd = %s,
#             spread_go = %s,
#             spread_pro = %s,
#             spread_vip = %s,
#             poderacion_go = %s,
#             poderacion_pro = %s,
#             poderacion_vip = %s,
#             "path" = %s,
#             fecha_insercion_precio = %s,
#             fecha_insercion_registro = %s
#         """)

#         for datos_update in new_ponderaciones_update:
#             #cursor.execute(rp_ponderacionxsymbol_python, datos_update)
#             print(datos_update)
            
#         #conexion.commit()
#         conexion.close()

#     else:
#         return 'Sin updates'
    
    
    
    
    
    
    
    
    
    
    
    
    
# instrumento = %s,
# tipo_instrumento = %s,
# tipo = '%s,
# precio = %s,
# tamano_contrato = %s,
# moneda_calculo = '%s',
# monto_usd = %s,
# spread_go = %s,
# spread_pro = %s,
# spread_vip = %s,
# poderacion_go = %s,
# poderacion_pro = %s,
# poderacion_vip = %s,
# "path" = %s,
# fecha_insercion_precio = %s,
# fecha_insercion_registro = %s