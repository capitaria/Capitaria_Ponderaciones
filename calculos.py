from datetime import timedelta # para agregar/quitar dias
from dateutil.relativedelta import relativedelta # para agregar/quitar mes

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
    # Se agrega los campos no calculados
    # "Path Instrumento", "Path Grupo", "Tatamano Contrato", "Moneda Calculo", "Spread Full"
    nuevas_ponderaciones = dict()

    for instrumento in ponderacion_base:
        nuevas_ponderaciones[instrumento] = {}

        for key, valor in ponderacion_base[instrumento].items():
            if key == 'path_instrumento':
                nuevas_ponderaciones[instrumento]['path_instrumento'] = valor
            if key == 'path_grupo':
                nuevas_ponderaciones[instrumento]['path_grupo'] = valor
            elif key == 'tamanio_1_lote':
                nuevas_ponderaciones[instrumento]['tamanio_contrato'] = valor
            elif key == 'moneda_base':
                nuevas_ponderaciones[instrumento]['moneda_calculo'] = valor
            elif key == 'spread_full':
                nuevas_ponderaciones[instrumento]['spread_full'] = int(valor)

    return nuevas_ponderaciones


def func_ponderaciones_campos_calculados(nuevas_ponderaciones,instrumentos_faltantes,calculo_a_usd):
    # Se agregan los campos calculados
    # "tipoinstrumento", "tipo", "monto_usd", "precio"
    for instrumento in nuevas_ponderaciones:
        nuevas_ponderaciones[instrumento]['tipo_instrumento'] = (
            func_tipo_instrumento(
                nuevas_ponderaciones[instrumento]['moneda_calculo'],
                nuevas_ponderaciones[instrumento]['path_instrumento']
            )
        )
        nuevas_ponderaciones[instrumento]['tipo'] = (
            func_tipo(
                nuevas_ponderaciones[instrumento]['path_instrumento']
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


def func_actualiza_path_instrumentos(instrumentos_mt5,instrumentos_path):
    # Verifica si el instrumento existe en la tabla reports.rp_ponderaciones_path
    # en caso de existir actualiza el "path instrumento" solo si fue cambiado
    # si el instrumento no existe lo crea en la misma tabla.
    insert = list()
    update = list()
    no_update = list()
            
    for instrumento in instrumentos_mt5: # Muestra los "instrumentos de MT5"
        if instrumento in instrumentos_path: # Si el "instrumento de MT5" esta en los "instrumentos de BDD"
            if instrumentos_mt5[instrumento]['path_instrumento'] != instrumentos_path[instrumento]['path_instrumento']: # Si el "Path Instrumento" de MT5 es distinto al "Path Instrumento" de la BDD
                update.append([instrumento,instrumentos_mt5[instrumento]['path_instrumento']])
            elif instrumentos_path[instrumento]['path_instrumento'][0:instrumentos_path[instrumento]['path_instrumento'].find("\\")] == 'Historicos' and instrumentos_path[instrumento]['path_grupo'] == '*': # Si el grupo instrumento "inicia en Historico" y el grupo path tiene "*", no actualiza 
                no_update.append([instrumento,instrumentos_path[instrumento]['path_instrumento']])
            elif instrumentos_path[instrumento]['path_instrumento'][0:instrumentos_path[instrumento]['path_instrumento'].find("\\")] != instrumentos_path[instrumento]['path_grupo'][0:instrumentos_path[instrumento]['path_grupo'].find("\\")]: # Si el "inicio del Path Instrumento" es distinto al "Inicio de Grupo Path"
                update.append([instrumento,instrumentos_path[instrumento]['path_instrumento']])
            else: # Si no es distinto, entonces no actualiza
                no_update.append([instrumento,instrumentos_mt5[instrumento]['path_instrumento']])
        else: # Si el "Instrumento MT5" no esta en "Instrumento BDD" entonces lo inserta
            insert.append([instrumento,instrumentos_mt5[instrumento]['path_instrumento'],instrumentos_mt5[instrumento]['fecha_insercion']])
            
    return insert, update, no_update


def func_actualiza_ponderaciones(viejas_ponderaciones,nuevas_ponderaciones):
    # va a buscar los nuevos instrumentos para ver si estan en la tabla, en caso de que esten va a recorrer los campos y ve si alguno cambio, para entonces actualizar, si no, no hay cambios, no actualizara el instrumento
    update = dict()
    no_update = dict()
    insert = dict()

    for codigo in nuevas_ponderaciones:
        if codigo in viejas_ponderaciones:
            if (viejas_ponderaciones[codigo]['precio'] != nuevas_ponderaciones[codigo]['precio']
                or viejas_ponderaciones[codigo]['spread_full'] != nuevas_ponderaciones[codigo]['spread_full']
                or viejas_ponderaciones[codigo]['spread_diff'] != nuevas_ponderaciones[codigo]['spread_diff']
                or viejas_ponderaciones[codigo]['spread_premium'] != nuevas_ponderaciones[codigo]['spread_premium']
                or viejas_ponderaciones[codigo]['spread_vip'] != nuevas_ponderaciones[codigo]['spread_vip']
                or viejas_ponderaciones[codigo]['grupos_id'] != nuevas_ponderaciones[codigo]['grupos_id']
                or viejas_ponderaciones[codigo]['monto_usd'] != nuevas_ponderaciones[codigo]['monto_usd']
                or viejas_ponderaciones[codigo]['path_instrumento'] != nuevas_ponderaciones[codigo]['path_instrumento']
                or viejas_ponderaciones[codigo]['path_grupo'] != nuevas_ponderaciones[codigo]['path_grupo']):
                update.update({codigo:nuevas_ponderaciones[codigo]})
            else:
                no_update.update({codigo:nuevas_ponderaciones[codigo]})
        else:
            insert.update({codigo:nuevas_ponderaciones[codigo]})
            
    return insert, update, no_update


def func_grupos_y_simbolos(grupos_reales,grupos_simbolos):
    #Une los grupos reales con los grupos de cada simbolo
    grupos = list()
    
    # grupo[0]:Numero Grupo - grupo[1]:Grupo - grupo[2]:Categoria - datos[1]:Path Instrumento - datos[2]:Spread Diferencia
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
    grupos_dict = {}

    for dato in grupos:
        agrupar = (dato[2], dato[3], dato[4]) # key -> dato[2]:Categoria - dato[3]:Grupo - dato[4]:Diferencia Spread
        if agrupar not in grupos_dict:
            grupos_dict[agrupar] = [dato[2], dato[3], dato[4], []]
        grupos_dict[agrupar][-1].append(dato[0])

    agrupacion = list(grupos_dict.values())
    
    return agrupacion


def func_agregar_spread_ponderaciones_premium_vip(nuevas_ponderaciones, agrupacion):
    # Agrega el Spread en base a las ponderaciones PREMIUM y VIP
    nuevas_ponderaciones2 = dict()

    for instrumento in nuevas_ponderaciones:
        path_grupo = nuevas_ponderaciones[instrumento]['path_grupo']
        for lista in agrupacion:
            if path_grupo == lista[1]:
                key = instrumento+lista[0]+str(lista[2])
                nuevas_ponderaciones2[key] = {
                    'instrumento' : instrumento,
                    'tipo_instrumento' : nuevas_ponderaciones[instrumento]['tipo_instrumento'],
                    'tipo' : nuevas_ponderaciones[instrumento]['tipo'],
                    'monto_usd' : nuevas_ponderaciones[instrumento]['monto_usd'],
                    'categoria' : lista[0],
                    'path_instrumento' : nuevas_ponderaciones[instrumento]['path_instrumento'],
                    'path_grupo' : nuevas_ponderaciones[instrumento]['path_grupo'],
                    'moneda_calculo' : nuevas_ponderaciones[instrumento]['moneda_calculo'],
                    'precio' : nuevas_ponderaciones[instrumento]['precio'],
                    'tamanio_contrato' : nuevas_ponderaciones[instrumento]['tamanio_contrato'],
                    'spread_full' : nuevas_ponderaciones[instrumento]['spread_full'],
                    'spread_diff' : lista[2],
                    'spread_premium' : nuevas_ponderaciones[instrumento]['spread_full'] + lista[2],
                    'spread_vip' : nuevas_ponderaciones[instrumento]['spread_full'] + lista[2],
                    'ponderacion_full' : float(1),
                    'ponderacion_premium' : func_ponderacion(nuevas_ponderaciones[instrumento]['spread_full'], lista[2], nuevas_ponderaciones[instrumento]['spread_full'] + lista[2]),
                    'ponderacion_vip' : func_ponderacion(nuevas_ponderaciones[instrumento]['spread_full'], lista[2], nuevas_ponderaciones[instrumento]['spread_full'] + lista[2]),
                    'grupos_id' : ', '.join(map(str, sorted(lista[3]))),
                    'fecha_insercion_precio' : nuevas_ponderaciones[instrumento]['fecha_insercion_precio'],
                    'fecha_insercion_registro' : nuevas_ponderaciones[instrumento]['fecha_insercion_registro']
                }
    return nuevas_ponderaciones2


def func_ponderacion(spread_full, spread_diff, spread_premium):
    #Calcula las Ponderaciones Pro y Premium (que siempre son las mismas)
    if (spread_full-spread_diff) > 0:
        ponderacion = round(spread_full/spread_premium,3)
    else:
        ponderacion = 1   
    return ponderacion

#^ OTROS
def func_mes_fiscal(fecha_consultada):
    # Fecha cae despues del 25, obtiene el mes fiscal exacto del proximo mes
    if fecha_consultada.day > 25:
        fecha_prox_mes_fiscal_exacta = fecha_consultada.replace(day=25) + relativedelta(months=1)
    # De lo contrario, el mes fiscal es el 25 del mes en curso
    else:
        fecha_prox_mes_fiscal_exacta = fecha_consultada.replace(day=25)
        
    # Fecha cae entre Lunes a Viernes
    if fecha_prox_mes_fiscal_exacta.weekday() >= 0 and fecha_prox_mes_fiscal_exacta.weekday() <= 4:
        # Fecha NO cae en Diciembre (ya que 25 es feriado)
        if fecha_prox_mes_fiscal_exacta.month != 12:
            fecha_prox_mes_fiscal_correcta = fecha_prox_mes_fiscal_exacta
        else:
            # Fecha cae entre Martes a Sabado, se resta 1 dia. 
            if fecha_prox_mes_fiscal_exacta.weekday() >= 1 and fecha_prox_mes_fiscal_exacta.weekday() <= 4:
                fecha_prox_mes_fiscal_correcta = (fecha_prox_mes_fiscal_exacta - timedelta(days=1))
            # De lo contrario cae Lunes, se resta 3 dias.
            else:
                fecha_prox_mes_fiscal_correcta = (fecha_prox_mes_fiscal_exacta - timedelta(days=3))
                
    #Fecha cae el Sabado, se resta 1 dia.
    elif fecha_prox_mes_fiscal_exacta.weekday() == 5:
        fecha_prox_mes_fiscal_correcta = (fecha_prox_mes_fiscal_exacta - timedelta(days=1))
    # De lo contrario cae el Domingo, se resta 2 dias.
    else:
        fecha_prox_mes_fiscal_correcta = (fecha_prox_mes_fiscal_exacta - timedelta(days=2))

    return fecha_prox_mes_fiscal_exacta, fecha_prox_mes_fiscal_correcta

def tiempo_exacto(xseg):
    minutos = xseg // 60
    segundos_restos = xseg % 60 # Obtengo los Segundos
    minutos_restos = minutos % 60 # Obtengo los Minutos
    return f"{round(minutos_restos)}m:{round(segundos_restos)}s"
#^ FIN OTROS