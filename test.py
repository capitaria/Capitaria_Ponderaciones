data = {'NK': {'path': 'CFD Indices\\Japon\\NK', 'poderacion_go': 1, 'moneda_calculo': 'JPY', 'tamanio_contrato': 10, 'spread_go': 2000, 'spread_pro': 1995, 'spread_vip': 1995, 'tipo_instrumento': 'INDICES', 'tipo': 'INDICES', 'precio': 33488.06, 'monto_usd': 0.0067, 'poderacion_pro': 0.998, 'poderacion_vip': 0.998},'NK2': {'path': 'CFD Indices\\Japon\\NK', 'poderacion_go': 1, 'moneda_calculo': 'JPY', 'tamanio_contrato': 10, 'spread_go': 2000, 'spread_pro': 1995, 'spread_vip': 1995, 'tipo_instrumento': 'INDICES', 'tipo': 'INDICES', 'precio': 33488.06, 'monto_usd': 0.0067, 'poderacion_pro': 0.998, 'poderacion_vip': 0.998}}

lista = list()
for i in data:
    datos = [
        i,
        data[i]['tipo_instrumento'],
        data[i]['tipo'],
        data[i]['precio'],
        data[i]['tamanio_contrato'],
        data[i]['moneda_calculo'],
        data[i]['monto_usd'],
        data[i]['spread_go'],
        data[i]['spread_pro'],
        data[i]['spread_vip'],
        data[i]['poderacion_go'],
        data[i]['poderacion_pro'],
        data[i]['poderacion_vip']
    ]
    lista.append(tuple(datos))

print(lista)