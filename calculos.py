# ponderacion_base = {
#     'T.NINTENDO': {
#         'path': 'CFD Acciones\\Tokio\\T.NINTENDO',
#         'moneda_base': 'JPY',
#         'tamanio_1_lote': 50,
#         'monto_operacion_min': 0.1,
#         'monto_operacion_max': 60.0,
#         'spread_pro': 1250.0,
#         'spread_premium': 1245.0,
#         'swap_compra': -2.9,
#         'swap_venta': -2.9
#         }
#     ,
#     'USDCLP': {
#         'path': 'Forex\\CLP\\USDCLP',
#         'moneda_base': 'USD',
#         'tamanio_1_lote': 100000,
#         'monto_operacion_min': 0.1,
#         'monto_operacion_max': 10.0,
#         'spread_pro': 0,
#         'spread_premium': -1.0,
#         'swap_compra': -9.0,
#         'swap_venta': 3.5
#         }
#     }

# precios = [('USDCLP', 867.8), ('T.NINTENDO', 6824.0)]

# monto_a_usd = {'usdclp': '868.35', 'usdpen': '3.731', 'usdcad': '1.363', 'eurusd': '1.09432', 'nzdusd': '0.6086', 'audusd': '0.6587', 'usdjpy': '149.45', 'gbpusd': '1.2609', 'usdchf': '0.8818', 'usdmxn': '17.1138'}

def func_tipo_instrumento(moneda, path):
    # Agrega el Tipo de Instrumento, tomando la moneda y el Path
    if 'ADR' in path:
        tipo_instrumento = 'ADR'
    elif 'Commodities' in path:
        tipo_instrumento = 'COMMODITIES'
    elif 'Criptomonedas' in path:
        tipo_instrumento = 'CRIPTOMONEDAS'
    elif 'ETF' in path:
        tipo_instrumento = 'ETF'
    elif 'Indices' in path:
        tipo_instrumento = 'INDICES'
    elif 'Forex' in path:
        tipo_instrumento = 'FOREX'
    elif 'Acciones' in path and 'JPY' in moneda:
        tipo_instrumento = 'ACCIONES TOKIO'
    elif 'Acciones' in path and 'CAD' in moneda:
        tipo_instrumento = 'ACCIONES CANADA'
    elif 'Acciones' in path and 'EUR' in moneda:
        tipo_instrumento = 'ACCIONES EUROPEAS'
    elif 'Acciones' in path and 'PENNY' in moneda:
        tipo_instrumento = 'ACCIONES EUROPEAS LONDRES'
    elif 'Acciones' in path and 'USD' in moneda:
        tipo_instrumento = 'ACCIONES USA'
    elif 'Acciones' in path and 'CLP' in moneda:
        tipo_instrumento = 'CFD CHILE'
    else:
        tipo_instrumento = 'N/A'
    
    return tipo_instrumento


def func_tipo(path):
    # Agrega el Tipo tomando solamente el Path
    if 'adr' in path.lower():
        tipo = 'ADR'
    elif 'commodities' in path.lower():
        tipo = 'COMMODITIES'
    elif 'criptomonedas' in path.lower():
        tipo = 'CRIPTO'
    elif 'etf' in path.lower():
        tipo = 'ETF'
    elif 'indices' in path.lower():
        tipo = 'INDICES'
    elif 'forex' in path.lower():
        tipo = 'FOREX'
    elif 'acciones' in path.lower():
        tipo = 'ACCIONES'
    else:
        tipo = 'N/A'
        
    return tipo


def func_precio(instrumento,precios):
    # Agrega el Precio cuando el instrumento, es igual al instrumento de la lista de precios
    for p in precios:
        if p[0] == instrumento:
            return p[1]

def func_monto_usd(moneda, monto_a_usd):
    # Calcula el valor del instrumento por dolar transado
    if moneda == 'CLP':
        for key, valor in monto_a_usd.items(): #key: usdclp / valor: 868.35
            if moneda.lower() in key:
                calculo_a_monto_usd = valor
    elif moneda == 'PEN':
        for key, valor in monto_a_usd.items():
            if moneda.lower() in key:
                calculo_a_monto_usd = round(1/float(valor),4)
    elif moneda == 'CAD':
        for key, valor in monto_a_usd.items():
            if moneda.lower() in key:
                calculo_a_monto_usd = round(1/float(valor),4)
    elif moneda == 'EUR':
        for key, valor in monto_a_usd.items():
            if moneda.lower() in key:
                calculo_a_monto_usd = round(1/float(valor),4)
    elif moneda == 'NZD':
        for key, valor in monto_a_usd.items():
            if moneda.lower() in key:
                calculo_a_monto_usd = round(1/float(valor),4)
    elif moneda == 'AUD':
        for key, valor in monto_a_usd.items():
            if moneda.lower() in key:
                calculo_a_monto_usd = round(1/float(valor),4)
    elif moneda == 'JPY':
        for key, valor in monto_a_usd.items():
            if moneda.lower() in key:
                calculo_a_monto_usd = round(1/float(valor),4)
    elif moneda == 'GBP':
        for key, valor in monto_a_usd.items():
            if moneda.lower() in key:
                calculo_a_monto_usd = round(1/float(valor),4)
    elif moneda == 'CHF':
        for key, valor in monto_a_usd.items():
            if moneda.lower() in key:
                calculo_a_monto_usd = round(1/float(valor),4)
    elif moneda == 'MXN':
        for key, valor in monto_a_usd.items():
            if moneda.lower() in key:
                calculo_a_monto_usd = round(1/float(valor),4)
    else:
        calculo_a_monto_usd = 1 # para USD es 1
    
    return calculo_a_monto_usd


def func_ponderacion(spread_pro, spread_go):
    #Calcula las Ponderaciones Pro y Premium (que siempre son las mismas)
    if spread_pro > 0:
        ponderacion = round(spread_pro/spread_go,3)
    else:
        ponderacion = 1
    
    return ponderacion


def func_ponderaciones_campos_no_calculados(ponderacion_base):
    #* Se agrega los campos no calculados (path, tatamano_contrato, moneda_calculo, spread_go, spread_pro, spread_vip y poderacion_go)
    nuevas_ponderaciones = dict()

    for instrumento in ponderacion_base:
        nuevas_ponderaciones[instrumento] = {}

        for key, valor in ponderacion_base[instrumento].items():
            if key == 'path':
                nuevas_ponderaciones[instrumento]['path'] = valor
            elif key == 'tamanio_1_lote':
                nuevas_ponderaciones[instrumento]['tamanio_contrato'] = valor
            elif key == 'moneda_base':
                nuevas_ponderaciones[instrumento]['moneda_calculo'] = valor
            elif key == 'spread_pro':
                nuevas_ponderaciones[instrumento]['spread_go'] = valor
            elif key == 'spread_premium':
                nuevas_ponderaciones[instrumento]['spread_pro'] = valor
                nuevas_ponderaciones[instrumento]['spread_vip'] = valor

            nuevas_ponderaciones[instrumento]['poderacion_go'] = 1

    return nuevas_ponderaciones


def func_ponderaciones_campos_calculados(nuevas_ponderaciones,precios,monto_a_usd):
    #* Se agrega los campos calculados (tipo_instrumento, tipo, precio, monto_usd, poderacion_pro y poderacion_vip)
    for instrumento in nuevas_ponderaciones:
        nuevas_ponderaciones[instrumento]['tipo_instrumento'] = func_tipo_instrumento(
            nuevas_ponderaciones[instrumento]['moneda_calculo'],
            nuevas_ponderaciones[instrumento]['path'])
        nuevas_ponderaciones[instrumento]['tipo'] = func_tipo(
            nuevas_ponderaciones[instrumento]['path'])
        nuevas_ponderaciones[instrumento]['precio'] = func_precio(
            instrumento,precios)
        nuevas_ponderaciones[instrumento]['monto_usd'] = func_monto_usd(
            nuevas_ponderaciones[instrumento]['moneda_calculo'],monto_a_usd)
        nuevas_ponderaciones[instrumento]['poderacion_pro'] = func_ponderacion(
            nuevas_ponderaciones[instrumento]['spread_pro'],
            nuevas_ponderaciones[instrumento]['spread_go'])
        nuevas_ponderaciones[instrumento]['poderacion_vip'] = nuevas_ponderaciones[instrumento]['poderacion_pro']

    return nuevas_ponderaciones


# data = func_ponderaciones_campos_no_calculados(ponderacion_base)
# print(func_ponderaciones_campos_calculados(data,precios,monto_a_usd))
