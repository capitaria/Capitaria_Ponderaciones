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
        tipo_instrumento = None
    
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
        tipo = None
        
    return tipo



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
    elif moneda == 'USD':
        for key, valor in monto_a_usd.items():
            if moneda.lower() in key:
                calculo_a_monto_usd = valor/valor
    else:
        calculo_a_monto_usd = None
    
    return calculo_a_monto_usd




def func_ponderaciones_campos_no_calculados(ponderacion_base):
    # Se agrega los campos no calculados (path, tatamano_contrato, moneda_calculo, spread_go (pro) y poderacion_go)

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
            elif key == 'spread_full':
                nuevas_ponderaciones[instrumento]['spread_full'] = int(valor)
            # elif key == 'spread_premium':
            #     nuevas_ponderaciones[instrumento]['spread_premium'] = 'test'
            # elif key == 'spread_premium':
            #     nuevas_ponderaciones[instrumento]['spread_pro'] = int(valor)
            #     nuevas_ponderaciones[instrumento]['spread_vip'] = int(valor)

            #nuevas_ponderaciones[instrumento]['poderacion_go'] = 1

    return nuevas_ponderaciones


def func_ponderaciones_campos_calculados(nuevas_ponderaciones,instrumentos_faltantes,calculo_a_usd):
    #* Se agrega los campos calculados (tipo_instrumento, tipo, precio, monto_usd)
    for instrumento in nuevas_ponderaciones:
        nuevas_ponderaciones[instrumento]['tipo_instrumento'] = (
            func_tipo_instrumento(
                nuevas_ponderaciones[instrumento]['moneda_calculo'],
                nuevas_ponderaciones[instrumento]['path']
            )
        )
        nuevas_ponderaciones[instrumento]['tipo'] = (
            func_tipo(
                nuevas_ponderaciones[instrumento]['path']
            )
        )
        nuevas_ponderaciones[instrumento]['monto_usd'] = (
            func_monto_usd(
                nuevas_ponderaciones[instrumento]['moneda_calculo'],calculo_a_usd
            )
        )

        for key, val in instrumentos_faltantes[instrumento].items():
            if key == 'precio':
                nuevas_ponderaciones[instrumento]['precio'] = round(val,4)
            elif key == 'fecha_insercion_precio':
                nuevas_ponderaciones[instrumento]['fecha_insercion_precio'] = val
            elif key == 'fecha_insercion_registro':
                nuevas_ponderaciones[instrumento]['fecha_insercion_registro'] = val

    return nuevas_ponderaciones

def func_actualiza_ponderaciones(viejas_ponderaciones,nuevas_ponderaciones):
    # va a buscar los nuevos instrumentos para ver si estan en la tabla, en caso de que esten va a recorrer los campos y ve si alguno cambio, para entonces actualizar, si no, no hay cambios, no actualizara el instrumento
    update = dict()
    no_update = dict()
    insert = dict()

    return nuevas_ponderaciones
    #todo - Aca debo ir a ver el codigo
    # for instrumento in nuevas_ponderaciones:
    #     if instrumento in viejas_ponderaciones:
    #         if viejas_ponderaciones[instrumento]['poderacion_pro'] != nuevas_ponderaciones[instrumento]['poderacion_pro'] or viejas_ponderaciones[instrumento]['precio'] != nuevas_ponderaciones[instrumento]['precio']:
    #             update.update({instrumento:nuevas_ponderaciones[instrumento]})
    #         else:
    #             no_update.update({instrumento:nuevas_ponderaciones[instrumento]})
    #     else:
    #         insert.update({instrumento:nuevas_ponderaciones[instrumento]})
            
    # return insert, update, no_update


def func_grupos_y_simbolos(grupos_reales,grupos_simbolos):
    #Une los grupos reales con los grupos de cada simbolo
    
    grupos = list()
    
    for grupo in grupos_reales:
        for datos in grupos_simbolos:
            if grupo[0] == datos[0]:
                grupos.append([
                    grupo[0],
                    grupo[1],
                    grupo[2],
                    datos[1],
                    datos[2] if datos[2] is not None else 0
                ])
    
    return grupos

def func_agrupacion_categoria(grupos):
    # Agrupa por Categoria
    
    grupos_dict = {} # Crear un diccionario para almacenar los grupos

    # Iterar sobre cada elemento de la lista
    for dato in grupos:
        agrupar = (dato[2], dato[3], dato[4])  # Definir la clave para la agrupación
        if agrupar not in grupos_dict:
            grupos_dict[agrupar] = [dato[2], dato[3], dato[4], []]
        grupos_dict[agrupar][-1].append(dato[0])

    # Obtener la lista final de listas
    agrupacion = list(grupos_dict.values())
    return agrupacion


def func_agregar_spread_ponderaciones_premium_vip(nuevas_ponderaciones, agrupacion):
    nuevas_ponderaciones2 = dict()

    # for lista in agrupacion:
    for instrumento in nuevas_ponderaciones:
        path = nuevas_ponderaciones[instrumento]['path']
        for lista in agrupacion:
            if path == lista[1]:
                #nuevas_ponderaciones[instrumento]
                key = instrumento+lista[0]+str(lista[2])
                nuevas_ponderaciones2[key] = {
                    'instrumento' : instrumento,
                    'tipo_instrumento' : nuevas_ponderaciones[instrumento]['tipo_instrumento'],
                    'tipo' : nuevas_ponderaciones[instrumento]['tipo'],
                    'monto_usd' : nuevas_ponderaciones[instrumento]['monto_usd'],
                    'categoria' : lista[0],
                    'path' : nuevas_ponderaciones[instrumento]['path'],
                    'moneda_calculo' : nuevas_ponderaciones[instrumento]['moneda_calculo'],
                    'precio' : nuevas_ponderaciones[instrumento]['precio'],
                    'tamanio_contrato' : nuevas_ponderaciones[instrumento]['tamanio_contrato'],
                    'spread_full' : nuevas_ponderaciones[instrumento]['spread_full'],
                    'spread_diff' : lista[2],
                    'spread_premium' : nuevas_ponderaciones[instrumento]['spread_full'] + lista[2],
                    'spread_vip' : nuevas_ponderaciones[instrumento]['spread_full'] + lista[2],
                    'ponderacion_full' : float(1),
                    'ponderacion_premium' : round((nuevas_ponderaciones[instrumento]['spread_full'] + lista[2]) / nuevas_ponderaciones[instrumento]['spread_full'],3),
                    'ponderacion_vip' : round((nuevas_ponderaciones[instrumento]['spread_full'] + lista[2]) / nuevas_ponderaciones[instrumento]['spread_full'],3),
                    'grupos_id' : ', '.join(map(str, lista[3])),
                    'fecha_insercion_precio' : nuevas_ponderaciones[instrumento]['fecha_insercion_precio'],
                    'fecha_insercion_registro' : nuevas_ponderaciones[instrumento]['fecha_insercion_registro']
                }
    return nuevas_ponderaciones2







def func_ponderacion(spread_pro, spread_go):
    #! Borrar
    #Calcula las Ponderaciones Pro y Premium (que siempre son las mismas)
    if spread_pro > 0:
        ponderacion = round(spread_pro/spread_go,3)
    else:
        ponderacion = 1
    
    return ponderacion