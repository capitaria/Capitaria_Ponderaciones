nuevas_ponderaciones = {'USDCLP': {'path_instrumento': 'Forex\\CLP\\USDCLP', 'path_grupo': 'Forex\\CLP\\USDCLP', 'moneda_calculo': 'USD', 'tamanio_contrato': 100000, 'spread_full': 0, 'tipo_instrumento': 'FOREX', 'tipo': 'FOREX', 'monto_usd': 1.0, 'precio': 962.4, 'fecha_insercion_precio': '2024-02-20 18:05:03.980', 'fecha_insercion_registro': '2024-02-21 17:20:51.394'}, '#NVDA': {'path_instrumento': 'CFD Acciones\\EEUU\\#NVDA', 'path_grupo': 'CFD Acciones\\EEUU\\*', 'moneda_calculo': 'USD', 'tamanio_contrato': 50, 'spread_full': 55, 'tipo_instrumento': 'ACCIONES USA', 'tipo': 'ACCIONES', 'monto_usd': 1.0, 'precio': 694.605, 'fecha_insercion_precio': '2024-02-20 18:05:03.980', 'fecha_insercion_registro': '2024-02-21 17:20:51.394'}, 'USDCOP': {'path_instrumento': 'Forex\\Minors\\USDCOP', 'path_grupo': 'Forex\\Minors\\USDCOP', 'moneda_calculo': 'USD', 'tamanio_contrato': 100000, 'spread_full': 0, 'tipo_instrumento': 'FOREX', 'tipo': 'FOREX', 'monto_usd': 1.0, 'precio': 3939.005, 'fecha_insercion_precio': '2024-02-20 18:05:03.980', 'fecha_insercion_registro': '2024-02-21 17:20:51.394'}}
agrupacion = [['FUL', 'Forex\\Minors\\USDCOP', 100, [583]], ['FUL', 'Forex*', 0, [583]], ['FUL', 'CFD*', 0, [583]]]

for instrumento in nuevas_ponderaciones:
    path_grupo = nuevas_ponderaciones[instrumento]['path_grupo']
    for lista in agrupacion:
        #print(path_grupo,lista[1])
        #path_grupo if path_grupo == lista[1] else path_grupo[:path_grupo.find(" ")] if path_grupo.find(" ") > 0 else path_grupo[:path_grupo.find("\\")] if path_grupo.find("\\") > 0 else '1'
        if path_grupo == lista[1] or path_grupo.find(" ") > 0 or path_grupo.find("\\") > 0:
            print(path_grupo)