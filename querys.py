
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
        -- and pr.symbol in ('USDCLP','T.NINTENDO','TSE.WEED','USDJPY')
    """
    cursor.execute(query_instrumentos_faltantes)
    query_instrumentos_faltantes = cursor.fetchall()

    instrumentos_faltantes = dict()

    for item in query_instrumentos_faltantes:
        instrumento = item[0]
        precio = item[1]
        fecha_insercion_precio = item[2]
        fecha_insercion_registro = item[3]
        instrumentos_faltantes[instrumento] = {
            'precio': round(float(precio),4),
            'fecha_insercion_precio' : fecha_insercion_precio,
            'fecha_insercion_registro' : fecha_insercion_registro,
        }
        
    return instrumentos_faltantes


def func_sel_generacion_data_base_mt5(conexion,instrumentos_faltantes):
    # Obtiene la base de los datos para despues calcular los datos
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
        null as spread_premium,
        ms."SwapLong" as swap_compra,
        ms."SwapShort" as swap_venta
    from
        mt5_symbols ms
    where
        ms."Symbol" in {tuple([x for x in instrumentos_faltantes]) if len([x for x in instrumentos_faltantes]) > 1 else f"('{[x for x in instrumentos_faltantes][0]}')"}
        and ms."Path" not ilike '%historicos%'
        and ms."Path" not ilike '%start%'
        and ms."Path" not ilike '%Alimentadores%'
        and ms."Path" not ilike '%Provisorios%'
        and ms."Path" not ilike '%MarketExecution%'
"""
    
    cursor.execute(query_mt5_symbols) # Ejecuta la query
    query_mt5_symbols = cursor.fetchall()
    
    ponderacion_base = dict()
    
    for item in query_mt5_symbols:
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
        ponderacion_base[symbol] = {
            'path': path,
            'moneda_base' : currencybase,
            'tamanio_1_lote' : int(contractsize),
            'monto_operacion_min' : round(volumemin,1),
            'monto_operacion_max' : round(volumemax,1),
            'spread_pro' : round(spread,1),
            'spread_premium' : None,
            'swap_compra': round(swaplong,4),
            'swap_venta': round(swapshort,4),
            }

    return ponderacion_base


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
    query_monto_moneda_a_usd = cursor.fetchall()

    monto_moneda_a_usd = dict()
    
    for item in query_monto_moneda_a_usd:
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
        monto_moneda_a_usd = {
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
        
        return monto_moneda_a_usd
    

def func_sel_instrumentos_old(conexion, instrumentos_faltantes):
    # Obtiene los instrumentods de la base de datos
    cursor = conexion.cursor()
    query_instrumentos_old = f"""
    select 
        instrumento,
        tipo_instrumento,
        tipo,
        precio,
        tamano_contrato,
        moneda_calculo,
        coalesce(monto_usd,0) as monto_usd,
        spread_go,
        spread_pro,
        spread_vip,
        poderacion_go,
        poderacion_pro,
        poderacion_vip,
        "path",
        fecha_insercion_precio,
        fecha_insercion_registro
    from 
        reports.rp_ponderacionxsymbol_python_update rppu
    where
        rppu.instrumento in {tuple([x for x in instrumentos_faltantes]) if len([x for x in instrumentos_faltantes]) > 1 else f"('{[x for x in instrumentos_faltantes][0]}')"}
    """
    cursor.execute(query_instrumentos_old)
    old_instrumentos = cursor.fetchall()

    viejas_ponderaciones = dict()
    
    for item in old_instrumentos:
        instrumento = item[0]
        tipo_instrumento = item[1]
        tipo = item[2]
        precio = item[3]
        tamanio_contrato = item[4]
        moneda_calculo = item[5]
        monto_usd = item[6]
        spread_go = item[7]
        spread_pro = item[8]
        spread_vip = item[9]
        poderacion_go = item[10]
        poderacion_pro = item[11]
        poderacion_vip = item[12]
        fecha_insercion_precio = item[13]
        viejas_ponderaciones[instrumento] = {
            'tipo_instrumento': tipo_instrumento,
            'tipo' : tipo,
            'precio' : round(precio,4),
            'tamanio_contrato' : int(tamanio_contrato),
            'moneda_calculo' : moneda_calculo,
            #'monto_usd' : round((monto_usd if monto_usd != None else 0),4),
            'monto_usd' : round(monto_usd,4),
            'spread_go' : round(spread_go,4),
            'spread_pro': round(spread_pro,4),
            'spread_vip': round(spread_vip,4),
            'poderacion_go': round(poderacion_go,4),
            'poderacion_pro': round(poderacion_pro,4),
            'poderacion_vip': round(poderacion_vip,4),
            'fecha_insercion_precio': fecha_insercion_precio,
            }
        
    return viejas_ponderaciones

def func_sel_grupos_reales(conexion):
    # Obtiene los IDs de grupos, el nombre de grupo y la categoria
    cursor = conexion.cursor()
    query_grupos_reales = f"""
    select 
        mg."Group_ID" as grupo_id,
        mg."Group" as grupo,
        case
            when mg."Group" ilike '%ful%' then 'FUL'
            when mg."Group" ilike '%vip%' then 'VIP'
            when mg."Group" ilike '%pre%' then 'PRE'
            else mg."Group"
        end as cat_grupo
    from
        mt5_groups mg
    where
        mg."Group" ilike 'real%'
        and mg."Group" not ilike '%lite%'
        and mg."Group" not ilike '%sta%'
        and mg."Group" not ilike '%ins%mesa%'
        and mg."Group_ID" not in (5,10,14) -- GRUPO NO ENCONTRADOS
        -- and mg."Group_ID" in (147,148,554) -- COMENTAR
    """

    cursor.execute(query_grupos_reales)
    query_grupos_reales = cursor.fetchall()
    
    grupos_reales = list()
    
    for item in query_grupos_reales:
        grupo_id = int(item[0])
        grupo = item[1]
        categoria_grupo = item[2]
        grupos_reales.append([
            grupo_id,
            grupo,
            categoria_grupo
        ])

    return grupos_reales


def func_sel_grupos_simbolos(conexion):
    # Obtiene los IDs de grupos, el nombre de grupo y la categoria
    cursor = conexion.cursor()
    query_grupos_simbolos = f"""
    select 
        mgs."Group_ID" as grupo_id_asoc,
        mgs."Path" as path,
        mgs."SpreadDiff" as spread_premium_diff
    from
        mt5_groups_symbols mgs
        -- where mgs."Group_ID" in (147,148) -- COMENTAR
    """

    cursor.execute(query_grupos_simbolos)
    query_grupos_simbolos = cursor.fetchall()
    
    grupos_simbolos = list()
    
    for item in query_grupos_simbolos:
        grupo_id_asoc = int(item[0])
        path = item[1]
        spread_premium_diff = item[2]
        grupos_simbolos.append([
            grupo_id_asoc,
            path,
            spread_premium_diff
        ])

    return grupos_simbolos

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
def func_ins_datos_ponderados(conexion, insert):
    # inserta en reports.rp_ponderacionxsymbol_python_update
    if len(insert) >= 1:
        new_ponderaciones_insert = list()
        for i in insert:
            datos = [
                i,
                insert[i]['tipo_instrumento'],
                insert[i]['tipo'],
                insert[i]['precio'],
                insert[i]['tamanio_contrato'],
                insert[i]['moneda_calculo'],
                insert[i]['monto_usd'],
                insert[i]['spread_go'],
                insert[i]['spread_pro'],
                insert[i]['spread_vip'],
                insert[i]['poderacion_go'],
                insert[i]['poderacion_pro'],
                insert[i]['poderacion_vip'],
                insert[i]['path'],
                insert[i]['fecha_insercion_precio'],
                insert[i]['fecha_insercion_registro']
            ]
            new_ponderaciones_insert.append(tuple(datos))
            
        cursor = conexion.cursor()
        
        rp_ponderacionxsymbol_python = (
        f"""
        INSERT INTO
        reports.rp_ponderacionxsymbol_python_update
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

        cursor.executemany(rp_ponderacionxsymbol_python,new_ponderaciones_insert)
        conexion.commit()
        cursor.close()
#^ FIN INSERT

#^ UPDATE
def func_upd_datos_ponderados(conexion, update):
    # actualiza en reports.rp_ponderacionxsymbol_python_update
    
    if len(update) >= 1:
        new_ponderaciones_update = list()
        for i in update:
            datos = [
                update[i]['tipo_instrumento'],
                update[i]['tipo'],
                update[i]['precio'],
                update[i]['tamanio_contrato'],
                update[i]['moneda_calculo'],
                update[i]['monto_usd'],
                update[i]['spread_go'],
                update[i]['spread_pro'],
                update[i]['spread_vip'],
                update[i]['poderacion_go'],
                update[i]['poderacion_pro'],
                update[i]['poderacion_vip'],
                update[i]['path'],
                update[i]['fecha_insercion_precio'],
                update[i]['fecha_insercion_registro'],
                i
            ]
            new_ponderaciones_update.append(datos)
            
        cursor = conexion.cursor()
    
        rp_ponderacionxsymbol_python = (
        f"""
        update
        reports.rp_ponderacionxsymbol_python_update
        set
            tipo_instrumento = %s,
            tipo = %s,
            precio = %s,
            tamano_contrato = %s,
            moneda_calculo = %s,
            monto_usd = %s,
            spread_go = %s,
            spread_pro = %s,
            spread_vip = %s,
            poderacion_go = %s,
            poderacion_pro = %s,
            poderacion_vip = %s,
            "path" = %s,
            fecha_insercion_precio = %s,
            fecha_insercion_registro = %s
        where
            instrumento = %s
        """)

        for datos_update in new_ponderaciones_update:
            cursor.execute(rp_ponderacionxsymbol_python, datos_update)
            #print(datos_update)    
            conexion.commit()
        
        conexion.close()

#^ FIN UPDATE

#^ INICIO HISTORICO
def func_ins_datos_ponderados_historicos(conexion, nuevas_ponderaciones):
    # inserta en reports.rp_ponderacionxsymbol_python_update
    if len(nuevas_ponderaciones) >= 1:
        new_ponderaciones_insert_historic = list()
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
            new_ponderaciones_insert_historic.append(tuple(datos))
            
        cursor = conexion.cursor()
        
        rp_ponderacionxsymbol_python = (
        f"""
        INSERT INTO
        reports.rp_ponderacionxsymbol_python_historical
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

        cursor.executemany(rp_ponderacionxsymbol_python,new_ponderaciones_insert_historic)
        conexion.commit()
        cursor.close()
#^ FIN INICIO HISTORICO