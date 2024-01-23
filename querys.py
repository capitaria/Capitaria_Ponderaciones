
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
        and pr.symbol in ('Cobre_Mar24','Palad_Mar24','Azu11_Mar24')
        -- and pr.symbol in ('USDCLP','T.NINTENDO','TSE.WEED','USDJPY','WTI','BRENT','#TSLA')
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
        ms."Symbol" as instrumento,
        ms."Path" as path_instrumento,
        rpp.path_grupo as path_grupo,
        ms."CurrencyBase" as moneda_base,
        ms."ContractSize" as tamaño_1_lote,
        ms."VolumeMin"/10000 as monto_operacion_min,
        ms."VolumeMax"/10000 as monto_operacion_max,
        ms."Spread" as spread_full,
        ms."SwapLong" as swap_compra,
        ms."SwapShort" as swap_venta
    from
        mt5_symbols ms inner join reports.rp_ponderaciones_path rpp
        on ms."Symbol" = rpp.instrumento
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
        instrumento = item[0]
        path_instrumento = item[1]
        path_grupo = item[2]
        currencybase = item[3]
        contractsize = item[4]
        volumemin = item[5]
        volumemax = item[6]
        spread_full = item[7]
        swaplong = item[8]
        swapshort = item[9]
        ponderacion_base[instrumento] = {
            'path_instrumento': path_instrumento,
            'path_grupo' : path_grupo,
            'moneda_base' : currencybase,
            'tamanio_1_lote' : int(contractsize),
            'monto_operacion_min' : round(volumemin,1),
            'monto_operacion_max' : round(volumemax,1),
            'spread_full' : round(spread_full,1),
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
        codigo,
        instrumento,
        tipo_instrumento,
        tipo,
        categoria,
        precio,
        tamano_contrato,
        moneda_calculo,
        coalesce(monto_usd,0) as monto_usd,
        spread_full,
        spread_diff,
        spread_premium,
        spread_vip,
        ponderacion_full,
        ponderacion_premium,
        ponderacion_vip,
        "path",
        grupos_id,
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
        codigo = item[0]
        # instrumento = item[1]
        # tipo_instrumento = item[2]
        # tipo = item[3]
        # categoria = item[4]
        precio = item[5]
        tamanio_contrato = item[6]
        # moneda_calculo = item[7]
        monto_usd = item[8]
        # spread_full = item[9]
        # spread_diff = item[10]
        # spread_premium = item[11]
        # spread_vip = item[12]
        ponderacion_full = item[13]
        ponderacion_premium = item[14]
        ponderacion_vip = item[15]
        # path = item[16]
        grupos_id = item[17]
        # fecha_insercion_precio = item[1]
        viejas_ponderaciones[codigo] = {
            # 'instrumento' : instrumento,
            # 'tipo_instrumento' : tipo_instrumento,
            # 'tipo' : tipo,
            # 'categoria' : categoria,
            'precio' : round(precio,4),
            'tamanio_contrato' : int(tamanio_contrato),
            # 'moneda_calculo' : moneda_calculo,
            # 'monto_usd' : round((monto_usd if monto_usd != None else 0),4),
            'monto_usd' : round(monto_usd,4),
            # 'spread_full' : round(spread_full,4),
            # 'spread_diff' : round(spread_diff,4),
            # 'spread_premium': round(spread_premium,4),
            # 'spread_vip': round(spread_vip,4),
            'ponderacion_full': round(ponderacion_full,4),
            'ponderacion_premium': round(ponderacion_premium,4),
            'ponderacion_vip': round(ponderacion_vip,4),
            # 'path' : path,
            'grupos_id' : grupos_id,
            # 'fecha_insercion_precio': fecha_insercion_precio,
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
	where mgs."Group_ID" in (
		select 
		    mg."Group_ID" as grupo_id
		from
		    mt5_groups mg
		where
		    mg."Group" ilike 'real%'
		    and mg."Group" not ilike '%lite%'
		    and mg."Group" not ilike '%sta%'
		    and mg."Group" not ilike '%ins%mesa%'
		    -- and mg."Group_ID" not in (5,10,14)
		    and mg."Group_ID" in (456)
	)
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
        for codigo in insert:
            datos = [
                codigo,
                insert[codigo]['instrumento'],
                insert[codigo]['tipo_instrumento'],
                insert[codigo]['tipo'],
                insert[codigo]['categoria'],
                insert[codigo]['precio'],
                insert[codigo]['tamanio_contrato'],
                insert[codigo]['moneda_calculo'],
                insert[codigo]['monto_usd'],
                insert[codigo]['spread_full'],
                insert[codigo]['spread_diff'],
                insert[codigo]['spread_premium'],
                insert[codigo]['spread_vip'],
                insert[codigo]['ponderacion_full'],
                insert[codigo]['ponderacion_premium'],
                insert[codigo]['ponderacion_vip'],
                insert[codigo]['path'],
                insert[codigo]['grupos_id'],
                insert[codigo]['fecha_insercion_precio'],
                insert[codigo]['fecha_insercion_registro']
            ]
            new_ponderaciones_insert.append(tuple(datos))
        
        cursor = conexion.cursor()
        
        rp_ponderacionxsymbol_python = (
        f"""
        INSERT INTO
        reports.rp_ponderacionxsymbol_python_update
        (
            codigo,
            instrumento,
            tipo_instrumento,
            tipo,
            categoria,
            precio,
            tamano_contrato,
            moneda_calculo,
            monto_usd,
            spread_full,
            spread_diff,
            spread_premium,
            spread_vip,
            ponderacion_full,
            ponderacion_premium,
            ponderacion_vip,
            path,
            grupos_id,
            fecha_insercion_precio,
            fecha_insercion_registro
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
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
        for codigo in update:
            datos = (
                update[codigo]['precio'],
                update[codigo]['monto_usd'],
                update[codigo]['spread_full'],
                update[codigo]['spread_diff'],
                update[codigo]['spread_premium'],
                update[codigo]['spread_vip'],
                update[codigo]['ponderacion_full'],
                update[codigo]['ponderacion_premium'],
                update[codigo]['ponderacion_vip'],
                update[codigo]['grupos_id'],
                update[codigo]['fecha_insercion_precio'],
                update[codigo]['fecha_insercion_registro'],
                codigo
            )
            new_ponderaciones_update.append(datos)
    
        query_update = (
        f"""
        update reports.rp_ponderacionxsymbol_python_update
        set
            precio = %s,
            monto_usd = %s,
            spread_full = %s,
            spread_diff = %s,
            spread_premium = %s,
            spread_vip = %s,
            ponderacion_full = %s,
            ponderacion_premium = %s,
            ponderacion_vip = %s,
            grupos_id = %s,
            fecha_insercion_precio = %s,
            fecha_insercion_registro = %s
        where
            codigo = %s
        """)

        cursor = conexion.cursor()
        
  
        # for datos_update in new_ponderaciones_update:
        #     print(datos_update)
        cursor.executemany(query_update, tuple(new_ponderaciones_update))

        conexion.commit()
        conexion.close()

#^ FIN UPDATE

#^ INICIO HISTORICO
def func_ins_datos_ponderados_historicos(conexion, nuevas_ponderaciones):
    # inserta en reports.rp_ponderacionxsymbol_python_update
    if len(nuevas_ponderaciones) >= 1:
        new_ponderaciones_insert_historic = list()
        for codigo in nuevas_ponderaciones:
            datos = [
                codigo,
                nuevas_ponderaciones[codigo]['instrumento'],
                nuevas_ponderaciones[codigo]['tipo_instrumento'],
                nuevas_ponderaciones[codigo]['tipo'],
                nuevas_ponderaciones[codigo]['categoria'],
                nuevas_ponderaciones[codigo]['precio'],
                nuevas_ponderaciones[codigo]['tamanio_contrato'],
                nuevas_ponderaciones[codigo]['moneda_calculo'],
                nuevas_ponderaciones[codigo]['monto_usd'],
                nuevas_ponderaciones[codigo]['spread_full'],
                nuevas_ponderaciones[codigo]['spread_diff'],
                nuevas_ponderaciones[codigo]['spread_premium'],
                nuevas_ponderaciones[codigo]['spread_vip'],
                nuevas_ponderaciones[codigo]['ponderacion_full'],
                nuevas_ponderaciones[codigo]['ponderacion_premium'],
                nuevas_ponderaciones[codigo]['ponderacion_vip'],
                nuevas_ponderaciones[codigo]['path'],
                nuevas_ponderaciones[codigo]['grupos_id'],
                nuevas_ponderaciones[codigo]['fecha_insercion_precio'],
                nuevas_ponderaciones[codigo]['fecha_insercion_registro']
            ]
            new_ponderaciones_insert_historic.append(tuple(datos))
            
            
        cursor = conexion.cursor()
        
        rp_ponderacionxsymbol_python = (
        f"""
        INSERT INTO
        reports.rp_ponderacionxsymbol_python_historical
        (
            codigo,
            instrumento,
            tipo_instrumento,
            tipo,
            categoria,
            precio,
            tamano_contrato,
            moneda_calculo,
            monto_usd,
            spread_full,
            spread_diff,
            spread_premium,
            spread_vip,
            ponderacion_full,
            ponderacion_premium,
            ponderacion_vip,
            path,
            grupos_id,
            fecha_insercion_precio,
            fecha_insercion_registro
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """)
    #return new_ponderaciones_insert_historic
        cursor.executemany(rp_ponderacionxsymbol_python,new_ponderaciones_insert_historic)
        conexion.commit()
        cursor.close()
#^ FIN INICIO HISTORICO