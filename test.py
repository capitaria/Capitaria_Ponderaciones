nuevas_ponderaciones = {'USDCLP': {'path_instrumento': 'Forex\\CLP\\USDCLP', 'path_grupo': 'Forex\\CLP\\USDCLP', 'moneda_calculo': 'USD', 'tamanio_contrato': 100000, 'spread_full': 0, 'tipo_instrumento': 'FOREX', 'tipo': 'FOREX', 'monto_usd': 1.0, 'precio': 962.4, 'fecha_insercion_precio': '2024-02-20 18:05:03.980', 'fecha_insercion_registro': '2024-02-21 17:20:51.394'},
                        '#NVDA': {'path_instrumento': 'CFD Acciones\\EEUU\\#NVDA', 'path_grupo': 'CFD Acciones\\EEUU\\*', 'moneda_calculo': 'USD', 'tamanio_contrato': 50, 'spread_full': 55, 'tipo_instrumento': 'ACCIONES USA', 'tipo': 'ACCIONES', 'monto_usd': 1.0, 'precio': 694.605, 'fecha_insercion_precio': '2024-02-20 18:05:03.980', 'fecha_insercion_registro': '2024-02-21 17:20:51.394'},
                        'USDCOP': {'path_instrumento': 'Forex\\Minors\\USDCOP', 'path_grupo': 'Forex\\Minors\\USDCOP', 'moneda_calculo': 'USD', 'tamanio_contrato': 100000, 'spread_full': 0, 'tipo_instrumento': 'FOREX', 'tipo': 'FOREX', 'monto_usd': 1.0, 'precio': 3939.005, 'fecha_insercion_precio': '2024-02-20 18:05:03.980', 'fecha_insercion_registro': '2024-02-21 17:20:51.394'}}
agrupacion = [['FUL', 'Forex\\Minors\\USDCOP', 100, [583]], ['FUL', 'Forex*', 0, [583]], ['FUL', 'CFD*', 0, [583]]]

# Agrega el Spread en base a las ponderaciones PREMIUM y VIP
nuevas_ponderaciones2 = dict()

for instrumento in nuevas_ponderaciones:
    path_grupo = nuevas_ponderaciones[instrumento]['path_grupo']
    for lista in agrupacion:
        #print(path_grupo in lista[1])
        #print(path_grupo[:path_grupo.find(" ")] in lista[1])
        #print(path_grupo[:path_grupo.find("\\")] in lista[1])
        # # # if path_grupo in lista[1]:
        # # #     print('A: ',path_grupo)
        # # # elif path_grupo[:path_grupo.find(" ")] in lista[1]:
        # # #     print('B: ',path_grupo[:path_grupo.find(" ")])
        # # # elif path_grupo[:path_grupo.find("\\")] in lista[1]:
        # # #     print('C: ',path_grupo[:path_grupo.find("\\")])
        #path_grupo if path_grupo == lista[1] else path_grupo[:path_grupo.find(" ")] if path_grupo.find(" ") > 0 else path_grupo[:path_grupo.find("\\")] if path_grupo.find("\\") > 0 else '1'
        if path_grupo == lista[1] or path_grupo[:path_grupo.find(" ")] in lista[1] or path_grupo[:path_grupo.find("\\")] in lista[1]:
            key = instrumento+lista[0]+str(lista[2])
            nuevas_ponderaciones2[key] = {
                # 'instrumento' : instrumento,
                # 'tipo_instrumento' : nuevas_ponderaciones[instrumento]['tipo_instrumento'],
                # 'tipo' : nuevas_ponderaciones[instrumento]['tipo'],
                # 'monto_usd' : nuevas_ponderaciones[instrumento]['monto_usd'],
                # 'categoria' : lista[0],
                # 'path_instrumento' : nuevas_ponderaciones[instrumento]['path_instrumento'],
                # 'path_grupo' : nuevas_ponderaciones[instrumento]['path_grupo'],
                # 'moneda_calculo' : nuevas_ponderaciones[instrumento]['moneda_calculo'],
                # 'precio' : nuevas_ponderaciones[instrumento]['precio'],
                # 'tamanio_contrato' : nuevas_ponderaciones[instrumento]['tamanio_contrato'],
                # 'spread_full' : nuevas_ponderaciones[instrumento]['spread_full'],
                # 'spread_diff' : lista[2],
                # 'spread_premium' : nuevas_ponderaciones[instrumento]['spread_full'] + lista[2],
                # 'spread_vip' : nuevas_ponderaciones[instrumento]['spread_full'] + lista[2],
                # 'ponderacion_full' : float(1),
                # #'ponderacion_premium' : func_ponderacion(nuevas_ponderaciones[instrumento]['spread_full'], lista[2], nuevas_ponderaciones[instrumento]['spread_full'] + lista[2]),
                # #'ponderacion_vip' : func_ponderacion(nuevas_ponderaciones[instrumento]['spread_full'], lista[2], nuevas_ponderaciones[instrumento]['spread_full'] + lista[2]),
                # 'grupos_id' : ', '.join(map(str, sorted(lista[3]))),
                # 'fecha_insercion_precio' : nuevas_ponderaciones[instrumento]['fecha_insercion_precio'],
                # 'fecha_insercion_registro' : nuevas_ponderaciones[instrumento]['fecha_insercion_registro']
            }
            
print(nuevas_ponderaciones2)
            
            
            
            


