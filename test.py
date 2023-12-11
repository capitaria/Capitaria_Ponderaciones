# old = {'USDCLP': {'tipo_instrumento': 'FOREX', 'tipo': 'FOREX', 'precio': 878.2, 'tamanio_contrato': 100000, 'moneda_calculo': 'USD   ', 'monto_usd': 1.0, 'spread_go': 0, 'spread_pro': -1, 'spread_vip': -1, 'poderacion_go': 1.0, 'poderacion_pro': 1.0, 'poderacion_vip': 1.0, 'fecha_insercion_precio': 'Forex\\CLP\\USDCLP'}, 'T.NINTENDO': {'tipo_instrumento': 'ACCIONES TOKIO', 'tipo': 'ACCIONES', 'precio': 6810.5, 'tamanio_contrato': 50, 'moneda_calculo': 'JPY   ', 'monto_usd': 0.0067, 'spread_go': 1250, 'spread_pro': 1245, 'spread_vip': 1245, 'poderacion_go': 1.0, 'poderacion_pro': 0.996, 'poderacion_vip': 0.996, 'fecha_insercion_precio': 'CFD Acciones\\Tokio\\T.NINTENDO'}}

# new = {'USDCLP': {'path': 'Forex\\CLP\\USDCLP', 'poderacion_go': 1, 'moneda_calculo': 'USD', 'tamanio_contrato': 100000, 'spread_go': 0, 'spread_pro': -1, 'spread_vip': -1, 'tipo_instrumento': 'FOREX', 'tipo': 'FOREX', 'monto_usd': 1.0, 'poderacion_pro': 1, 'poderacion_vip': 1, 'precio': 871.5000, 'fecha_insercion_precio': '2023-12-07 18:05:07.524', 'fecha_insercion_registro': '2023-12-08 17:42:03.747'}, 'TSE.WEED': {'path': 'CFD Acciones\\Toronto\\TSE.WEED', 'poderacion_go': 1, 'moneda_calculo': 'CAD', 'tamanio_contrato': 50, 'spread_go': 11, 'spread_pro': 6, 'spread_vip': 6, 'tipo_instrumento': 'ACCIONES CANADA', 'tipo': 'ACCIONES', 'monto_usd': 0.7337, 'poderacion_pro': 0.545, 'poderacion_vip': 0.545, 'precio': 0.9850, 'fecha_insercion_precio': '2023-12-07 18:05:07.524', 'fecha_insercion_registro': '2023-12-08 17:42:03.747'}, 'T.NINTENDO': {'path': 'CFD Acciones\\Tokio\\T.NINTENDO', 'poderacion_go': 1, 'moneda_calculo': 'JPY', 'tamanio_contrato': 50, 'spread_go': 1250, 'spread_pro': 1245, 'spread_vip': 1245, 'tipo_instrumento': 'ACCIONES TOKIO', 'tipo': 'ACCIONES', 'monto_usd': 0.0067, 'poderacion_pro': 0.996, 'poderacion_vip': 0.996, 'precio': 6871.5000, 'fecha_insercion_precio': '2023-12-07 18:05:07.524', 'fecha_insercion_registro': '2023-12-08 17:42:03.747'},'USDJPY': {'path': 'Forex\\CLP\\USDCLP', 'poderacion_go': 1, 'moneda_calculo': 'USD', 'tamanio_contrato': 100000, 'spread_go': 0, 'spread_pro': -1, 'spread_vip': -1, 'tipo_instrumento': 'FOREX', 'tipo': 'FOREX', 'monto_usd': 1.0, 'poderacion_pro': 1, 'poderacion_vip': 1, 'precio': 871.5000, 'fecha_insercion_precio': '2023-12-07 18:05:07.524', 'fecha_insercion_registro': '2023-12-08 17:42:03.747'}}


# for n in new:
#     #print(n)
#     if n in old: # si el instrumetno nuevo esta en los antiguos?
#         # si (ahora deberia ver si actualizo algo)

#         if old[n]['poderacion_pro'] != new[n]['poderacion_pro']: # Si la ponderacion es disinta
#             # Debe actualizar valores
#             print('SI',n,':',old[n]['poderacion_pro'],'-',new[n]['poderacion_pro'])
#         else:
#             # No debe actualizar
#             print('NO',n,':',old[n]['poderacion_pro'],'-',new[n]['poderacion_pro'])
#     else: 
#         #no, asi que debe insertarse
#         #print(n,new[n])
#         continue










# Diccionario de origen
diccionario_origen = {'clave1': 'valor1', 'clave2': 'valor2'}

# Diccionario de destino
diccionario_destino = {}

# Clave que deseas mover
clave_a_mover = 'clave1'

# Verificar si la clave existe en el diccionario de origen
if clave_a_mover in diccionario_origen:
    # Extraer el valor asociado a la clave
    valor_moved = diccionario_origen.pop(clave_a_mover)
    
    # Agregar la clave y valor al diccionario de destino
    diccionario_destino[clave_a_mover] = valor_moved

    # Imprimir los diccionarios después de la operación
    print("Diccionario de origen:", diccionario_origen)
    print("Diccionario de destino:", diccionario_destino)
else:
    print(f"La clave '{clave_a_mover}' no existe en el diccionario de origen.")
