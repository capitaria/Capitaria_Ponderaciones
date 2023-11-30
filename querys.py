from con.connection import psql

def func_generacion_data_base_mt5(conexion):
    # Obtiene la base de los datos para despues calcular los datos
    cursor = conexion.cursor()
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
    
        
def func_obtener_precio(conexion):
    # Obtiene los precios segun cada instrumento
    cursor = conexion.cursor()
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

    return precioxsymbol

def func_monto_moneda_usd(conexion):
    # Obtiene motod dolarizado segun la moneda
    cursor = conexion.cursor()
    monto_moneda_a_usd = f"""
    select
        usd_price as usdclp,
        pen_price as usdpen,
        usdcad,
        eurusd,
        nzdusd,
        audusd,
        usdjpy,
        gbpusd,
        usdchf,
        usdmxn
    from
        processes.pr_fiscal_period 
    order by
        fecha_inicio desc
        fetch first 1 row only
    """
    cursor.execute(monto_moneda_a_usd) # Ejecuta la query
    monto_a_usd = cursor.fetchall()

    calculo_a_usd = dict()
    
    for item in monto_a_usd:
        usdclp = item[0]
        usdpen = item[1]
        usdcad = item[2]
        eurusd = item[3]
        nzdusd = item[4]
        audusd = item[5]
        usdjpy = item[6]
        gbpusd = item[7]
        usdchf = item[8]
        usdmxn = item[9]
        calculo_a_usd = {
            'usdclp' : round(usdclp,5),
            'usdpen' : round(usdpen,5),
            'usdcad' : round(usdcad,5),
            'eurusd' : round(eurusd,5),
            'nzdusd' : round(nzdusd,5),
            'audusd' : round(audusd,5),
            'usdjpy' : round(usdjpy,5),
            'gbpusd' : round(gbpusd,5),
            'usdchf' : round(usdchf,5),
            'usdmxn' : round(usdmxn,5),
            # nota: tambien se puede ocupar 'usdmxn' : '{:.5f}'.format(usdmxn), pero la diferencia esta en que si o si te deja los 5 decimales y si no los tiene, los rellena con 0
            }
        
        return calculo_a_usd