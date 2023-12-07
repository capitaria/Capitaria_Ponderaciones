from con.connection import psql

#& SELECT
def func_sel_instrumentos_faltantes(conexion):
    # Obtiene los instrumentos y precio de pr_precios
    cursor = conexion.cursor()
    query_instrumentos_faltantes = f"""
    select
        pr.symbol as instrumento,
        round(((pr.bidlast + pr.asklast)/2)::numeric,4) as precio,
        TO_CHAR(pr.fecha_insercion, 'YYYY-MM-DD HH24:MI:SS.MS') as fecha_insercion_precio,
        TO_CHAR(NOW(), 'YYYY-MM-DD HH24:MI:SS.MS') as fecha_insercion_registro
    from
        reports.rp_precios pr
    where
        pr.fecha_insercion::date = now()::date - interval '1 day'
        and (pr.symbol not like '%x0%'
        and pr.symbol not like '%x2%'
        and pr.symbol not like '%x4%')
        limit 100
    """
    cursor.execute(query_instrumentos_faltantes)
    instrumentos_faltantes = cursor.fetchall()

    instrumentos_faltantes_dict = dict()

    for item in instrumentos_faltantes:
        instrumento = item[0]
        precio = item[1]
        fecha_insercion_precio = item[2]
        fecha_insercion_registro = item[3]
        instrumentos_faltantes_dict[instrumento] = {
            'precio': precio,
            'fecha_insercion_precio' : fecha_insercion_precio,
            'fecha_insercion_registro' : fecha_insercion_registro,
        }
        
    return instrumentos_faltantes_dict


def func_sel_generacion_data_base_mt5(conexion,instrumentos_faltantes):
    # Obtiene la base de los datos para despues calcular los datos

    #return instrumentos_faltantes

    
    cursor = conexion.cursor()
    query_mt5_symbols = f"""
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
        ms."Symbol" in {tuple([x for x in instrumentos_faltantes]) if len([x for x in instrumentos_faltantes]) > 1 else f"('{[x for x in instrumentos_faltantes][0]}')"}
        /*and ms."Path" not ilike '%historicos%'
        and ms."Path" not ilike '%start%'
        and ms."Path" not ilike '%Alimentadores%'
        and ms."Path" not ilike '%Provisorios%'
        and ms."Path" not ilike '%MarketExecution%'*/
"""
    
    cursor.execute(query_mt5_symbols) # Ejecuta la query
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
            'swap_venta': round(swapshort,4),
            }

    return ponderaciones
    
#! se debe eliminar
# def func_sel_obtener_precio(conexion, instrumentos_faltantes):
#     # Obtiene los precios segun cada instrumento
#     cursor = conexion.cursor()
#     query_precio_x_symbol = f"""
#     select
#         trim(rp.instrumento) as symbol,
#         rp.precio as precio
#     from
#         reports.rp_ponderacionxsymbol rp
#     where trim(rp.instrumento) in {instrumentos_faltantes}
#     """
# #,'#TSLA','TSE.WEED','#ADR_SQM','WTI','UK100','ETF_XLY'
#     cursor.execute(query_precio_x_symbol) # Ejecuta la query
#     precio_x_symbol = cursor.fetchall()

#     return precio_x_symbol

def func_sel_monto_moneda_usd(conexion):
    # Obtiene motod dolarizado segun la moneda
    cursor = conexion.cursor()
    query_monto_moneda_a_usd = f"""
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
    cursor.execute(query_monto_moneda_a_usd) # Ejecuta la query
    monto_moneda_a_usd = cursor.fetchall()

    calculo_a_usd = dict()
    
    for item in monto_moneda_a_usd:
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
            }
        
        return calculo_a_usd
    

#! Se debe borrar
# def func_sel_campos_rp_ponderacionxsymbol_python(conexion):
#     # Obtiene los campos de la tabla
#     cursor = conexion.cursor()
#     ponderacionxsymbol_python = f"""
#         select
#             column_name
#         from
#             information_schema.columns
#         where
#         table_name = 'rp_ponderacionxsymbol_python'
#     """

#     cursor.execute(ponderacionxsymbol_python)
#     campos = cursor.fetchall()

#     campos = tuple([c[0] for c in campos])

#     return campos

#& FIN SELECT


#^ INSERT
def func_ins_datos_ponderados(conexion, nuevas_ponderaciones):
    # inserta en reports.rp_ponderacionxsymbol_python
    
    new_ponderaciones = list()
    for i in nuevas_ponderaciones:
        datos = [
            i,
            nuevas_ponderaciones[i]['tipo_instrumento'],
            nuevas_ponderaciones[i]['tipo'],
            nuevas_ponderaciones[i]['precio'],
            nuevas_ponderaciones[i]['tamanio_contrato'],
            nuevas_ponderaciones[i]['moneda_calculo'],
            nuevas_ponderaciones[i]['monto_usd'],
            nuevas_ponderaciones[i]['spread_go'],
            nuevas_ponderaciones[i]['spread_pro'],
            nuevas_ponderaciones[i]['spread_vip'],
            nuevas_ponderaciones[i]['poderacion_go'],
            nuevas_ponderaciones[i]['poderacion_pro'],
            nuevas_ponderaciones[i]['poderacion_vip'],
            nuevas_ponderaciones[i]['path'],
            nuevas_ponderaciones[i]['fecha_insercion_precio'],
            nuevas_ponderaciones[i]['fecha_insercion_registro']
        ]
        new_ponderaciones.append(tuple(datos))

    cursor = conexion.cursor()
    
    rp_ponderacionxsymbol_python = (
    f"""
    INSERT INTO reports.rp_ponderacionxsymbol_python
    (
        instrumento,
        tipo_instrumento,
        tipo,
        precio,
        tamano_contrato,
        moneda_calculo,
        monto_usd,
        spread_go,
        spread_pro,
        spread_vip,
        poderacion_go,
        poderacion_pro,
        poderacion_vip,
        path,
        fecha_insercion_precio,
        fecha_insercion_registro
    )
    VALUES
    (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    """)

    cursor.executemany(rp_ponderacionxsymbol_python,new_ponderaciones)
    conexion.commit()
    cursor.close()
    
#^ FIN INSERT



