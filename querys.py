
#& SELECT
def func_sel_mt5_instrumento_path(conexion):
    # Obtiene todos los "instrumentos" y "path instrumento" de la tabla mt5_symbols.
    cursor = conexion.cursor()
    query_instrumento_path = """
	select 
		ms."Symbol" as symbol,
		ms."Path" as path_instrumento,
        TO_CHAR(NOW(), 'YYYY-MM-DD HH24:MI:SS.MS') as fecha_insercion_registro
	from 
		mt5_symbols ms
    order by
        ms."Symbol" asc
    """
    cursor.execute(query_instrumento_path)
    query_instrumento_path = cursor.fetchall()

    instrumentos_path = dict()

    for item in query_instrumento_path:
        instrumento = item[0]
        path_instrumento = item[1]
        fecha_insercion = item[2]
        instrumentos_path[instrumento] = {
            'path_instrumento' : path_instrumento,
            'fecha_insercion' : fecha_insercion
        }
        
    return instrumentos_path


def func_sel_path_instrumento(conexion):
    # Obtiene todos los "instrumentos" y "path instrumento" de la tabla python_extract.py_rp_ponderaciones_path
    cursor = conexion.cursor()
    query_instrumentos = """
	select 
		rpp.instrumento,
        rpp.path_instrumento,
        rpp.path_grupo
	from
		python_extract.py_rp_ponderaciones_path rpp
    order by rpp.instrumento asc
    """
    cursor.execute(query_instrumentos)
    query_instrumentos = cursor.fetchall()
    
    instrumentos_path = dict()
    
    for item in query_instrumentos:
        instrumento = item[0]
        path_instrumento = item[1]
        path_grupo = item[2]
        instrumentos_path[instrumento] = {
            'path_instrumento' : path_instrumento,
            'path_grupo' : path_grupo
        }
        
    return instrumentos_path


def func_sel_path_grupo_faltante(conexion,update_path):
    # Obtiene los "Path Grupo" que son null o algun path que venga en el update_path.
    # IMPORTANTE: el "Path Grupo" sirve para obtener la diferencia de Spread.
    cursor = conexion.cursor()
    query_path_grupos_faltantes = f"""
    select 
        rpp.instrumento,
        rpp.path_instrumento,
        rpp.path_grupo
    from
        python_extract.py_rp_ponderaciones_path rpp
    where
        rpp.path_grupo is null
        or rpp.path_grupo = ''
        or rpp.instrumento in 
        {tuple([x[0] for x in update_path]) if len(update_path) > 1 else
        f"('{[x[0] for x in update_path][0]}')" if len(update_path) == 1 else "('')"}
    """
    
    cursor.execute(query_path_grupos_faltantes)
    query_path_grupos_faltantes = cursor.fetchall()
    path_grupos_faltantes = [[path_grupo[0],path_grupo[1]] for path_grupo in query_path_grupos_faltantes]
    
    return path_grupos_faltantes


def func_sel_grupos_existentes(conexion):
    # Obtiene los "Path Grupo" que existen en la tabla mt5_groups_symbols
    cursor = conexion.cursor()
    query_path_grupos_existentes = """
    select 
        distinct mgs."Path" 
    from
        mt5_groups_symbols mgs
    order by
        1 asc
    """
    cursor.execute(query_path_grupos_existentes)
    query_path_grupos_existentes = cursor.fetchall()
    
    path_grupos_existentes = [path_grupo[0] for path_grupo in query_path_grupos_existentes]
    
    return path_grupos_existentes


def func_llenado_path_grupo(paths_grupos_faltantes, paths_grupos):
    # Llena el "Path Grupo" dependiendo del "Path Instrumento"
    path_grupos_new = list()

    for instrumento, path_instrumento in paths_grupos_faltantes:
        if path_instrumento in paths_grupos: #busca el path de instrumento, en el path de grupo
            path_grupo = path_instrumento
            path_grupos_new.append([instrumento,path_grupo])
        else:
            path_new_grupo = path_instrumento[:-len(instrumento)]+'*' # le agrega el * al final del path
            if path_new_grupo in paths_grupos:
                path_grupo = path_new_grupo
                path_grupos_new.append([instrumento,path_grupo])
            else:
                path_new_grupo = path_new_grupo[:-2] # En caso de no encontrarlo, busca el "/"
                N = path_new_grupo.find('\\')+1
                path_grupo = path_new_grupo[:N]+'*'
                if path_new_grupo in paths_grupos:
                    path_grupo = path_new_grupo
                    path_grupos_new.append([instrumento,path_grupo])    
                else:
                    if path_grupo in paths_grupos:
                        path_grupo = path_grupo
                        path_grupos_new.append([instrumento,path_grupo])
    
    return path_grupos_new


def func_sel_instrumentos_faltantes(conexion, fecha_consultada):
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
            pr.fecha_insercion::date = '{fecha_consultada}'
            and pr.symbol in
            (
                select 
                    ppp.instrumento
                from
                    python_extract.py_rp_ponderaciones_path ppp
                -- where
                    -- ppp.path_grupo not in ('START\*','Provisorios\*','*','MarketExecution\*','Alimentadores\*','Acc Chile\*')
            )
    """
    
    # -- now()::date
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
        mt5_symbols ms inner join python_extract.py_rp_ponderaciones_path rpp
        on ms."Symbol" = rpp.instrumento
    where
        ms."Symbol" in {tuple([x for x in instrumentos_faltantes]) if len([x for x in instrumentos_faltantes]) > 1 else f"('{[x for x in instrumentos_faltantes][0]}')"}
        -- and ms."Path" not ilike '%historicos%'
        -- and ms."Path" not ilike '%start%'
        -- and ms."Path" not ilike '%Alimentadores%'
        -- and ms."Path" not ilike '%Provisorios%'
        -- and ms."Path" not ilike '%MarketExecution%'
        -- and ms."Symbol" not in ('USDCLP', 'USDCLPabr24', 'USDCLPmar24', 'USDCLPmay24', 'USDCOP')
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


# def func_sel_monto_moneda_usd(conexion, fecha_consultada):
#     # Obtiene motod dolarizado segun la moneda
#     cursor = conexion.cursor()
#     query_monto_moneda_a_usd = f"""
#     select
#         usd_price as usdclp,
#         pen_price as usdpen,
#         usdcad,
#         eurusd,
#         nzdusd,
#         audusd,
#         usdjpy,
#         gbpusd,
#         usdchf,
#         usdmxn,
#         fecha_inicio,
# 	    fecha_fin
#     from
#         processes.pr_fiscal_period 
#     where
#         '{fecha_consultada}' between fecha_inicio and fecha_fin
#     order by
#         fecha_inicio desc
#         fetch first 1 row only
#     """
#     cursor.execute(query_monto_moneda_a_usd) # Ejecuta la query
#     query_monto_moneda_a_usd = cursor.fetchall()

#     monto_moneda_a_usd = dict()
    
#     for item in query_monto_moneda_a_usd:
#         usdclp = item[0]
#         usdpen = item[1]
#         usdcad = item[2]
#         eurusd = item[3]
#         nzdusd = item[4]
#         audusd = item[5]
#         usdjpy = item[6]
#         gbpusd = item[7]
#         usdchf = item[8]
#         usdmxn = item[9]
#         inicio = item[10].strftime("%d-%m-%Y %H:%M:%S")
#         fin = item[11].strftime("%d-%m-%Y %H:%M:%S")
#         monto_moneda_a_usd = {
#             'usdclp' : round(usdclp,5),
#             'usdpen' : round(usdpen,5),
#             'usdcad' : round(usdcad,5),
#             'eurusd' : round(eurusd,5),
#             'nzdusd' : round(nzdusd,5),
#             'audusd' : round(audusd,5),
#             'usdjpy' : round(usdjpy,5),
#             'gbpusd' : round(gbpusd,5),
#             'usdchf' : round(usdchf,5),
#             'usdmxn' : round(usdmxn,5),
#             'intervalo' : f"{inicio} al {fin}",
#             }
        
#         return monto_moneda_a_usd
    
def func_sel_precio_divisas(conexion, fecha_consultada):
    # Obtiene el precio de las monedas al dia consultado
    cursor = conexion.cursor()
    query_monto_moneda_a_usd = f"""
    select
        pr.symbol as instrumento,
        round(((pr.bidlast + pr.asklast)/2)::numeric,4) as precio,
        TO_CHAR(pr.fecha_insercion, 'YYYY-MM-DD') as fecha_insercion_precio
    from
        reports.rp_precios pr
    where
        pr.symbol in ('AUDUSD','USDBRL','USDCHF','EURUSD','GBPUSD','USDJPY','NZDUSD','USDCAD','USDCLP')
        and pr.fecha_insercion::date = '{fecha_consultada}'
    """
    cursor.execute(query_monto_moneda_a_usd) # Ejecuta la query
    query_monto_moneda_a_usd = cursor.fetchall()

    monto_moneda_a_usd = dict()
    
    for item in query_monto_moneda_a_usd:
        instrumento = item[0]
        precio = item[1]
        fecha = item[2]
        monto_moneda_a_usd[instrumento] = {
            'precio': round(float(precio),4),
            'fecha' : fecha
        }
        
    return monto_moneda_a_usd


def func_sel_grupos_reales(conexion):
    # Obtiene los IDs de grupos, el nombre de grupo y la categoria de mt5_groups
    # Ademas solo obtiene los grupos donde existen Subcuentas asociadas
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
        end as cat_grupo,
        count(mu."Login") as logins
    from
        mt5_groups mg left join mt5_users mu
        on mg."Group" = mu."Group"
    where
        mg."Group" ilike 'real%'
        and mg."Group" not ilike '%lite%'
        and mg."Group" not ilike '%sta%'
        and mg."Group" not ilike '%ins%mesa%'
        and mg."Group" not like '%99'
        -- and mg."Group_ID" in (165, 166) -- COMENTAR
    group by
        mg."Group_ID",
        mg."Group",
        cat_grupo
    having
        count(mu."Login") != 0
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
    # Obtiene los IDs de grupos, el nombre de grupo y la categoria de mt5_groups_symbols
    cursor = conexion.cursor()
    query_grupos_simbolos = f"""
    select 
        mgs."Group_ID" as grupo_id_asoc,
        mgs."Path" as path,
        coalesce(mgs."SpreadDiff",0) as spread_diff
    from
        mt5_groups_symbols mgs
    where mgs."Group_ID" in 
        (
        select 
            mg."Group_ID" as grupo_id
        from
            mt5_groups mg left join mt5_users mu
            on mg."Group" = mu."Group"
        where
            mg."Group" ilike 'real%'
            and mg."Group" not ilike '%lite%'
            and mg."Group" not ilike '%sta%'
            and mg."Group" not ilike '%ins%mesa%'
            and mg."Group" not like '%99' -- COMENTAR
            -- and mgs."Group_ID" in (165, 166) -- COMENTAR
            -- and mgs."Path" = 'Forex\\Minors\\USDCOP' -- COMENTAR
        group by
            mg."Group_ID"
        having
            count(mu."Login") != 0   
        )
    """

    cursor.execute(query_grupos_simbolos)
    query_grupos_simbolos = cursor.fetchall()
    
    grupos_simbolos = list()
    
    for item in query_grupos_simbolos:
        grupo_id_asoc = int(item[0])
        path = item[1]
        spread_diff = item[2]
        grupos_simbolos.append([
            grupo_id_asoc,
            path,
            spread_diff
        ])

    return grupos_simbolos
#& FIN SELECT

#^ INSERT
def func_ins_instrumento_path(conexion, insert):
    # inserta en python_extract.py_rp_ponderaciones_path
    if len(insert) >= 1:
        insert = [tuple(datos) for datos in insert]
        
        cursor = conexion.cursor()
        
        rp_ponderaciones_path = (
        """
        INSERT INTO
        python_extract.py_rp_ponderaciones_path
        (
            instrumento,
            path_instrumento,
            fecha_insercion
        )
        VALUES
        (
            %s, %s, %s
        )
        """)

        cursor.executemany(rp_ponderaciones_path,insert)
        conexion.commit()
        cursor.close()
        
        
def func_upd_path_grupo(conexion, llenado_path_grupo):
    # actualiza python_extract.rp_ponderacionxsymbol_python_update
    # como el instrumento ya esta insertado y el path es nulo, pareciera que inserta...
    if len(llenado_path_grupo) >= 1:
        for clave, valor in llenado_path_grupo:
            query_llenado_path_grupo = (
            """
            update
                python_extract.py_rp_ponderaciones_path
            set
                path_grupo = %s
            where
                instrumento = %s
            """)
            
            cursor = conexion.cursor()
            cursor.execute(query_llenado_path_grupo, (valor, clave))

        conexion.commit()
        #conexion.close()
        

def func_ins_datos_ponderados_historicos(conexion, nuevas_ponderaciones):
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
                nuevas_ponderaciones[codigo]['tamano_contrato'],
                nuevas_ponderaciones[codigo]['moneda_calculo'],
                nuevas_ponderaciones[codigo]['monto_usd'],
                nuevas_ponderaciones[codigo]['spread_categoria'],
                nuevas_ponderaciones[codigo]['spread_diff_categoria'],
                nuevas_ponderaciones[codigo]['ponderacion_categoria'],
                nuevas_ponderaciones[codigo]['path_instrumento'],
                nuevas_ponderaciones[codigo]['path_grupo'],
                nuevas_ponderaciones[codigo]['grupos_id'],
                nuevas_ponderaciones[codigo]['fecha_insercion_precio'],
                nuevas_ponderaciones[codigo]['fecha_insercion_registro']
            ]
            new_ponderaciones_insert_historic.append(tuple(datos))
            
        cursor = conexion.cursor()
        
        rp_ponderacionxsymbol_python = (
        """
        INSERT INTO
        python_extract.py_rp_ponderacionxsymbol_historical
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
            spread_categoria,
            spread_diff_categoria,
            ponderacion_categoria,
            path_instrumento,
            path_grupo,
            grupos_id,
            fecha_insercion_precio,
            fecha_insercion_registro
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """)
        
        cursor.executemany(rp_ponderacionxsymbol_python,new_ponderaciones_insert_historic)
        conexion.commit()
        cursor.close()
        

def func_ins_datos_ponderados(conexion, update):
    cursor = conexion.cursor()    
    query_truncate = "truncate table python_extract.py_rp_ponderacionxsymbol_update_fiscal"
    cursor.execute(query_truncate)
    conexion.commit()
    
    new_ponderaciones_update = list()
    for codigo in update:
        datos = [
            codigo,
            update[codigo]['instrumento'],
            update[codigo]['tipo_instrumento'],
            update[codigo]['tipo'],
            update[codigo]['categoria'],
            update[codigo]['precio'],
            update[codigo]['tamano_contrato'],
            update[codigo]['moneda_calculo'],
            update[codigo]['monto_usd'],
            update[codigo]['spread_categoria'],
            update[codigo]['spread_diff_categoria'],
            update[codigo]['ponderacion_categoria'],
            update[codigo]['path_instrumento'],
            update[codigo]['path_grupo'],
            update[codigo]['grupos_id'],
            update[codigo]['fecha_insercion_precio'],
            update[codigo]['fecha_insercion_registro']
        ]
        new_ponderaciones_update.append(tuple(datos))
    
    cursor = conexion.cursor()
    
    rp_ponderacionxsymbol_python = (
    """
    INSERT INTO
    python_extract.py_rp_ponderacionxsymbol_update_fiscal
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
        spread_categoria,
        spread_diff_categoria,
        ponderacion_categoria,
        path_instrumento,
        path_grupo,
        grupos_id,
        fecha_insercion_precio,
        fecha_insercion_registro
    )
    VALUES
    (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    """)

    cursor.executemany(rp_ponderacionxsymbol_python,new_ponderaciones_update)
    conexion.commit()
    cursor.close()


def func_upd_path_instrumento(conexion, update):
    # Actualiza el "path instrumento" en python_extract.py_rp_ponderaciones_path
    if len(update) >= 1:
        for clave, valor in update:
            query_update_path = (
            """
            update
                python_extract.py_rp_ponderaciones_path
            set
                path_instrumento = %s
            where
                instrumento = %s
            """)
            
            cursor = conexion.cursor()
            cursor.execute(query_update_path, (valor, clave))
        
        conexion.commit()


def func_ins_datos_ponderados_diarios(conexion, update):
    cursor = conexion.cursor()    
    query_truncate = "truncate table python_extract.py_rp_ponderacionxsymbol"
    cursor.execute(query_truncate)
    conexion.commit()
    
    new_ponderaciones_update = list()
    for codigo in update:
        datos = [
            codigo,
            update[codigo]['instrumento'],
            update[codigo]['tipo_instrumento'],
            update[codigo]['tipo'],
            update[codigo]['categoria'],
            update[codigo]['precio'],
            update[codigo]['tamano_contrato'],
            update[codigo]['moneda_calculo'],
            update[codigo]['monto_usd'],
            update[codigo]['spread_categoria'],
            update[codigo]['spread_diff_categoria'],
            update[codigo]['ponderacion_categoria'],
            update[codigo]['path_instrumento'],
            update[codigo]['path_grupo'],
            update[codigo]['grupos_id'],
            update[codigo]['fecha_insercion_precio'],
            update[codigo]['fecha_insercion_registro']
        ]
        new_ponderaciones_update.append(tuple(datos))
    
    cursor = conexion.cursor()
    
    rp_ponderacionxsymbol_python = (
    """
    INSERT INTO
    python_extract.py_rp_ponderacionxsymbol
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
        spread_categoria,
        spread_diff_categoria,
        ponderacion_categoria,
        path_instrumento,
        path_grupo,
        grupos_id,
        fecha_insercion_precio,
        fecha_insercion_registro
    )
    VALUES
    (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    """)

    cursor.executemany(rp_ponderacionxsymbol_python,new_ponderaciones_update)
    conexion.commit()
    cursor.close()
    
    
    
    
    
    
    
    
    
#! OBSOLETO
# def func_upd_datos_ponderados(conexion, update):    
#     if len(update) >= 1:
#         new_ponderaciones_update = list()
#         for codigo in update:
#             datos = (
#                 update[codigo]['instrumento'],
#                 update[codigo]['tipo_instrumento'],
#                 update[codigo]['tipo'],
#                 update[codigo]['categoria'],
#                 update[codigo]['precio'],
#                 update[codigo]['tamano_contrato'],
#                 update[codigo]['moneda_calculo'],
#                 update[codigo]['monto_usd'],
#                 update[codigo]['spread_categoria'],
#                 update[codigo]['spread_diff_categoria'],
#                 update[codigo]['ponderacion_categoria'],
#                 update[codigo]['path_instrumento'],
#                 update[codigo]['path_grupo'],
#                 update[codigo]['grupos_id'],
#                 update[codigo]['fecha_insercion_precio'],
#                 update[codigo]['fecha_insercion_registro'],
#                 codigo
#             )
#             new_ponderaciones_update.append(datos)
    
#         query_update = (
#         f"""
#         update python_extract.py_rp_ponderacionxsymbol_update_fiscal
#         set
#             instrumento = %s
#             tipo_instrumento = %s
#             tipo = %s
#             categoria = %s
#             precio = %s
#             tamano_contrato = %s
#             moneda_calculo = %s
#             monto_usd = %s
#             spread_categoria = %s
#             spread_diff_categoria = %s
#             ponderacion_categoria = %s
#             path_instrumento = %s
#             path_grupo = %s
#             grupos_id = %s
#             fecha_insercion_precio = %s
#             fecha_insercion_registro = %s
#         where
#             codigo = %s
#         """)

#         cursor = conexion.cursor()
#         cursor.executemany(query_update, tuple(new_ponderaciones_update))

#         conexion.commit()
#         conexion.close()


# def func_sel_instrumentos_old_historical(conexion, instrumentos_faltantes, fecha_consultada):
#     # Obtiene los instrumentods de la base de datos de la tabla py_rp_ponderacionxsymbol_historical
#     def func_fecha_maxima_historical(conexion):
#         # Obitiene la fecha Maxima de la insercion de la tabla py_rp_ponderacionxsymbol_historical
#         cursor = conexion.cursor()
#         query_fecha_max = f"""(
#             select
#                 max(fecha_insercion_registro)::date
#             from
#                 reports.py_rp_ponderacionxsymbol_historical prph
#             where
#                 fecha_insercion_registro::date < '{fecha_consultada}'
#         )"""
#         cursor.execute(query_fecha_max)
#         fecha_max = cursor.fetchall()
#         return fecha_max
    
#     fecha_maxima = func_fecha_maxima_historical(conexion)
#     fecha_maxima = fecha_maxima[0][0]
#     fecha_maxima = fecha_maxima.strftime("%Y-%m-%d") if fecha_maxima is not None else '1987-10-24'
    
#     cursor = conexion.cursor()
#     query_instrumentos_old = f"""
#     select 
#         codigo,
#         precio,
#         tamano_contrato,
#         coalesce(monto_usd,0) as monto_usd,
#         spread_categoria,
#         ponderacion_categoria,
#         path_instrumento,
#         path_grupo,
#         grupos_id
#     from 
#         reports.py_rp_ponderacionxsymbol_historical
#     where
#         fecha_insercion_registro::date = '{fecha_maxima}'
#         and instrumento in {tuple([x for x in instrumentos_faltantes]) if len([x for x in instrumentos_faltantes]) > 1 else f"('{[x for x in instrumentos_faltantes][0]}')"}
#     """
#     cursor.execute(query_instrumentos_old)
#     old_instrumentos = cursor.fetchall()

#     viejas_ponderaciones = dict()
    
#     for item in old_instrumentos:
#         codigo = item[0]
#         precio = item[1]
#         tamano_contrato = item[2]
#         monto_usd = item[3]
#         spread_categoria = item[4]
#         ponderacion_categoria = item[5]
#         path_instrumento = item[6]
#         path_grupo = item[7]
#         grupos_id = item[8]
#         viejas_ponderaciones[codigo] = {
#             'precio' : round(precio,4),
#             'tamano_contrato' : int(tamano_contrato),
#             'monto_usd' : round(monto_usd,4),
#             'spread_categoria' : round(spread_categoria,4),
#             'ponderacion_categoria': round(ponderacion_categoria,4),
#             'path_instrumento' : path_instrumento,
#             'path_grupo' : path_grupo,
#             'grupos_id' : grupos_id
#             }
        
#     return viejas_ponderaciones


# def func_sel_instrumentos_old_update(conexion, instrumentos_faltantes):
#     # Obtiene los instrumentods de la base de datos de la tabla python_extract.py_rp_ponderacionxsymbol_update_fiscal
#     cursor = conexion.cursor()
#     query_instrumentos_old = f"""
#         select
#             codigo,
#             instrumento,
#             tipo_instrumento,
#             tipo,
#             categoria,
#             precio,
#             tamano_contrato,
#             moneda_calculo,
#             coalesce(monto_usd,0) as monto_usd,
#             spread_categoria,
#             spread_diff_categoria,
#             ponderacion_categoria,
#             path_instrumento,
#             path_grupo,
#             grupos_id,
#             fecha_insercion_precio,
#             fecha_insercion_registro
#         from 
#             python_extract.py_rp_ponderacionxsymbol_update_fiscal pppu
#         where
#             pppu.instrumento in {tuple([x for x in instrumentos_faltantes]) if len([x for x in instrumentos_faltantes]) > 1 else f"('{[x for x in instrumentos_faltantes][0]}')"}
#     """
#     cursor.execute(query_instrumentos_old)
#     old_instrumentos = cursor.fetchall()

#     viejas_ponderaciones = dict()
    
#     for item in old_instrumentos:
#         codigo = item[0]
#         instrumento = item[1]
#         tipo_instrumento = item[2]
#         tipo = item[3]
#         categoria = item[4]
#         precio = item[5]
#         tamano_contrato = item[6]
#         moneda_calculo = item[7]
#         monto_usd = item[8]
#         spread_categoria = item[9]
#         spread_diff_categoria = item[10]
#         ponderacion_categoria = item[11]
#         path_instrumento = item[12]
#         path_grupo = item[13]
#         grupos_id = item[14]
#         viejas_ponderaciones[codigo] = {
#             'instrumento' : instrumento,
#             'tipo_instrumento' : tipo_instrumento,
#             'tipo' : tipo,
#             'categoria' : categoria,
#             'precio' : round(precio,4),
#             'tamano_contrato' : int(tamano_contrato),
#             'moneda_calculo' : moneda_calculo,
#             'monto_usd' : round(monto_usd,4),
#             'spread_categoria' : round(spread_categoria,4),
#             'spread_diff_categoria' : round(spread_diff_categoria,4),
#             'ponderacion_categoria': round(ponderacion_categoria,4),
#             'path_instrumento' : path_instrumento,
#             'path_grupo' : path_grupo,
#             'grupos_id' : grupos_id
#             }
        
#     return viejas_ponderaciones