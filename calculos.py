ponderacion_base = {
    'T.NINTENDO': {
        'path': 'CFD Acciones\\Tokio\\T.NINTENDO',
        'moneda_base': 'JPY',
        'tamanio_1_lote': 50,
        'monto_operacion_min': 0.1,
        'monto_operacion_max': 60.0,
        'spread_pro': 1250,
        'spread_premium': 1245.0,
        'swap_compra': -2.9,
        'swap_venta': -2.9
        },
    'USDCLP': {
        'path': 'Forex\\CLP\\USDCLP',
        'moneda_base': 'USD',
        'tamanio_1_lote': 100000,
        'monto_operacion_min': 0.1,
        'monto_operacion_max': 10.0,
        'spread_pro': 0,
        'spread_premium': -1.0,
        'swap_compra': -9.0,
        'swap_venta': 3.5
        }
    }

def tipo_instrumento(valor):
    return(valor)

def calculo_ponderaciones(ponderacion_base):
    nuevas_ponderaciones = dict()

    for instrumento in ponderacion_base:
        nuevas_ponderaciones[instrumento] = {}

        for key, valor in ponderacion_base[instrumento].items():
            if key == 'tamanio_1_lote':
                nuevas_ponderaciones[instrumento]['tamano_contrato'] = valor
            elif key == 'moneda_base':
                nuevas_ponderaciones[instrumento]['moneda_calculo'] = valor
            else:
                nuevas_ponderaciones[instrumento]['tipo_instrumento'] = None # Se calcula
                nuevas_ponderaciones[instrumento]['tipo'] = None # Se calcula
                nuevas_ponderaciones[instrumento]['precio'] = None # Se calcula
                nuevas_ponderaciones[instrumento]['monto_usd'] = None # Se calcula
                nuevas_ponderaciones[instrumento]['poderacion_pro'] = None # Se calcula
                nuevas_ponderaciones[instrumento]['poderacion_vip'] = None # Se calcula
                

    return nuevas_ponderaciones

print(calculo_ponderaciones(ponderacion_base))




   
        #         'tamano_contrato' : None,
        #         'moneda_calculo' : None,
        #         'spread_go' : None,
        #         'spread_pro' : None,
        #         'spread_vip' : None,
        #         'poderacion_go' : None,