nuevas_ponderaciones = {'WTI': {'path': 'CFD Commodities\\Spot\\WTI', 'poderacion_go': 1, 'moneda_calculo': 'USD', 'tamanio_contrato': 1000, 'spread_full': 200, 'tipo_instrumento': 'COMMODITIES', 'tipo': 'COMMODITIES', 'monto_usd': 1.0, 'precio': 73.85, 'fecha_insercion_precio': '2024-01-18 18:05:07.444', 'fecha_insercion_registro': '2024-01-19 09:59:56.473'}
                        ,'BRENT': {'path': 'CFD Commodities\\Spot\\BRENT', 'poderacion_go': 1, 'moneda_calculo': 'CLP', 'tamanio_contrato': 1000, 'spread_full': 50, 'tipo_instrumento': 'COMMODITIES', 'tipo': 'COMMODITIES', 'monto_usd': 1.0, 'precio': 78.63, 'fecha_insercion_precio': '2024-01-18 18:05:07.444', 'fecha_insercion_registro': '2024-01-19 10:01:17.806'}
                        }
agrupacion = [['VIP', 'CFD Commodities\\Spot\\WTI', -50, [147]], ['PRE', 'CFD Commodities\\Spot\\WTI', -50, [450, 554]], ['VIP', 'CFD Commodities\\Spot\\WTI', 0, [148]],
              ['VIP', 'CFD Commodities\\Spot\\BRENT', -20, [147,148]], ['PRE', 'CFD Commodities\\Spot\\BRENT', -50, [450, 554]]]


nuevas_ponderaciones2 = dict()

# for lista in agrupacion:
for instrumento in nuevas_ponderaciones:
    path = nuevas_ponderaciones[instrumento]['path']
    for lista in agrupacion:
        
        if path == lista[1]:
            key = instrumento+lista[0]+str(lista[2])
            nuevas_ponderaciones2[key] = {
                # 'symbol' : instrumento,
                # 'tipo_instrumento' : nuevas_ponderaciones[instrumento]['tipo_instrumento'],
                # 'tipo' : nuevas_ponderaciones[instrumento]['tipo'],
                # 'monto_usd' : nuevas_ponderaciones[instrumento]['monto_usd'],
                # 'categoria' : lista[0],
                # 'path' : nuevas_ponderaciones[instrumento]['path'],
                # 'moneda_calculo' : nuevas_ponderaciones[instrumento]['moneda_calculo'],
                # 'precio' : nuevas_ponderaciones[instrumento]['precio'],
                # 'tamanio_contrato' : nuevas_ponderaciones[instrumento]['tamanio_contrato'],
                # 'spread_full' : nuevas_ponderaciones[instrumento]['spread_full'],
                # 'spread_diff' : lista[2],
                # 'spread_premium' : nuevas_ponderaciones[instrumento]['spread_full'] + lista[2],
                # 'spread_vip' : nuevas_ponderaciones[instrumento]['spread_full'] + lista[2],
                # 'ponderacion_full' : float(1),
                # 'ponderacion_premium' : (nuevas_ponderaciones[instrumento]['spread_full'] + lista[2]) / nuevas_ponderaciones[instrumento]['spread_full'],
                # 'ponderacion_vip' : (nuevas_ponderaciones[instrumento]['spread_full'] + lista[2]) / nuevas_ponderaciones[instrumento]['spread_full'],
                'grupos_id' : ', '.join(map(str, lista[3])),
                #'fecha_insercion_precio' : nuevas_ponderaciones[instrumento]['fecha_insercion_precio'],
                #'fecha_insercion_registro' : nuevas_ponderaciones[instrumento]['fecha_insercion_registro']
            }
print(nuevas_ponderaciones2)


# for a in agrupacion:
#     print(', '.join(map(str, a[3])))
