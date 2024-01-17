# nuevas_ponderaciones = {'WTI': {'path': 'CFD Commodities\\Spot\\WTI', 'poderacion_go': 1, 'moneda_calculo': 'USD', 'tamanio_contrato': 1000, 'spread_go': 200}}
# agrupacion = [['VIP', 'CFD Commodities\\Spot\\WTI', -50, [147]], ['PRE', 'CFD Commodities\\Spot\\WTI', -50, [450, 554]], ['VIP', 'CFD Commodities\\Spot\\WTI', 0, [148]]]

# for lista in agrupacion:
#     for instrumento in nuevas_ponderaciones:
#         if lista[1] == nuevas_ponderaciones[instrumento]['path']:
#             nuevas_ponderaciones[instrumento]['categoria'] = lista[0]
#             nuevas_ponderaciones[instrumento]['spread_dif'] = lista[2]
#             nuevas_ponderaciones[instrumento]['spread_premium'] = 'pre'
#             nuevas_ponderaciones[instrumento]['spread_vip'] = 'vip'
#             nuevas_ponderaciones[instrumento]['grupos_id'] = lista[3]
#         print(nuevas_ponderaciones)

nuevas_ponderaciones = {'WTI': {'path': 'CFD Commodities\\Spot\\WTI', 'poderacion_go': 1, 'moneda_calculo': 'USD', 'tamanio_contrato': 1000, 'spread_full': 200}
                        ,'BRENT': {'path': 'CFD Commodities\\Spot\\BRENT', 'poderacion_go': 1, 'moneda_calculo': 'CLP', 'tamanio_contrato': 1000, 'spread_full': 50}
                        }
agrupacion = [['VIP', 'CFD Commodities\\Spot\\WTI', -50, [147]], ['PRE', 'CFD Commodities\\Spot\\WTI', -50, [450, 554]], ['VIP', 'CFD Commodities\\Spot\\WTI', 0, [148]],
              ['VIP', 'CFD Commodities\\Spot\\BRENT', -20, [147,148]], ['PRE', 'CFD Commodities\\Spot\\BRENT', -50, [450, 554]]]


nuevas_ponderaciones2 = dict()

# for lista in agrupacion:
for instrumento in nuevas_ponderaciones:
    path = nuevas_ponderaciones[instrumento]['path']
    for lista in agrupacion:
        if path == lista[1]:
            nuevas_ponderaciones[instrumento]['symbol'] = instrumento
            nuevas_ponderaciones[instrumento]['categoria'] = lista[0]
            nuevas_ponderaciones[instrumento]['spread_diff'] = lista[2]
            nuevas_ponderaciones[instrumento]['spread_premium'] = nuevas_ponderaciones[instrumento]['spread_full'] + lista[2]
            nuevas_ponderaciones[instrumento]['spread_vip'] = nuevas_ponderaciones[instrumento]['spread_full'] + lista[2]
            nuevas_ponderaciones[instrumento]['ponderacion_premium'] = nuevas_ponderaciones[instrumento]['spread_premium'] / nuevas_ponderaciones[instrumento]['spread_full']
            nuevas_ponderaciones[instrumento]['ponderacion_vip'] = nuevas_ponderaciones[instrumento]['ponderacion_premium']
            nuevas_ponderaciones[instrumento]['grupos_id'] = lista[3]
            print(nuevas_ponderaciones[instrumento])