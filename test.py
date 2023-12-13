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





import psycopg2
from psycopg2 import sql

# Configura tus credenciales de la base de datos
dbname = 'nombre_de_tu_base_de_datos'
user = 'tu_usuario'
password = 'tu_contraseña'
host = 'localhost'

# Establece la conexión con la base de datos
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)

# Crea un cursor para ejecutar consultas SQL
cursor = conn.cursor()

# Datos de actualización masiva (puedes obtener estos datos de una fuente externa)
datos_actualizacion = [
    {'id': 1, 'columna1': 'nuevo_valor1', 'columna2': 'nuevo_valor2'},
    {'id': 2, 'columna1': 'otro_valor1', 'columna2': 'otro_valor2'},
    # Agrega más filas según sea necesario
]

# Itera sobre los datos de actualización y ejecuta la consulta de actualización
for datos in datos_actualizacion:
    # Construye la consulta UPDATE utilizando SQL dinámico
    query = sql.SQL("UPDATE nombre_de_la_tabla SET {} WHERE id = %s").format(
        sql.SQL(', ').join(
            [sql.Identifier(columna) + sql.SQL(' = %s') for columna in datos.keys() if columna != 'id']
        )
    )

    # Concatena los valores de las columnas (excluyendo 'id')
    valores = [datos[columna] for columna in datos.keys() if columna != 'id']

    # Añade el valor del 'id' al final de la lista de valores
    valores.append(datos['id'])

    # Ejecuta la consulta con los parámetros
    cursor.execute(query, valores)

# Guarda los cambios en la base de datos
conn.commit()

# Cierra el cursor y la conexión
cursor.close()
conn.close()
