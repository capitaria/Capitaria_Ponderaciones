from con.connection import psql

def generacion_data_base_mt5(conexion):
    cursor = conexion.cursor() # Crear cursor
    # Query a postgreSQL
    query_mt5 = f"""
    select
        ms."Symbol" as nemo,
        ms."Path" as path,
        ms."CurrencyBase" as moneda_base,
        ms."ContractSize" as tamaño_1_lote,
        ms."VolumeMin"/10000 as monto_operacion_min,
        ms."VolumeMax"/10000 as monto_operacion_max,
        ms."Spread" as spread_pro,
        ms."Spread" - ms."SwapMode" as spread_premium,
        ms."SwapLong" as swap_compra,
        ms."SwapShort" as swap_venta
    from
        mt5_symbols ms
    where
        ms."Path" not ilike '%historicos%'
        and ms."Path" not ilike '%start%'
        and ms."Path" not ilike '%Alimentadores%'
        and ms."Path" not ilike '%Provisorios%'
        and ms."Path" not ilike '%MarketExecution%'
        and ms."Symbol" in ('USDCLP', 'T.NINTENDO')
    """
# ,'#TSLA','TSE.WEED','#ADR_SQM','WTI','UK100','ETF_XLY'

    cursor.execute(query_mt5) # Ejecuta la query
    mt5_symbols = cursor.fetchall()
    
    ponderaciones = dict()
    
    for item in mt5_symbols:
        symbol = item[0]
        path = item[1]
        currencybase = item[2]
        contractsize = item[3]
        volumemin = item[4]
        volumemax = item[5]
        spread = item[6]
        swapmode = item[7]
        swaplong = item[8]
        swapshort = item[9]
        ponderaciones[symbol] = {
            'path': path,
            'moneda_base' : currencybase,
            'tamanio_1_lote' : int(contractsize),
            'monto_operacion_min' : round(volumemin,1),
            'monto_operacion_max' : round(volumemax,1),
            'spread_pro' : round(spread,1),
            'spread_premium' : round(swapmode,1),
            'swap_compra': round(swaplong,4),
            'swap_venta': round(swapshort,4)
            }

    return ponderaciones
    

    # ('USDCLP', 'T.NINTENDO' ,'#TSLA','TSE.WEED','#ADR_SQM','WTI','UK100','ETF_XLY')

        
def obtener_precio(conexion):
    cursor = conexion.cursor() # Crear cursor
    # Query a postgreSQL
    precioxsymbol = f"""
    select
        trim(rp.instrumento) as symbol,
        rp.precio as precio
    from
        reports.rp_ponderacionxsymbol rp
    where
        trim(rp.instrumento) in ('USDCLP', 'T.NINTENDO')
    """
#,'#TSLA','TSE.WEED','#ADR_SQM','WTI','UK100','ETF_XLY'
    cursor.execute(precioxsymbol) # Ejecuta la query
    precioxsymbol = cursor.fetchall()

    precios = dict()

    for item in precioxsymbol:
        symbol = item[0]
        precio = item[1]
        precios[symbol] = {
            'precio' : precio,
            }

    return precios
