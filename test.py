# Permite ver los grupos falntastes, para llenar de forma automatizada los path de los grupos faltantes

paths_grupos = ['*','Acciones\\#AAPL','Alimentadores\\*','CFD*','CFD Acciones\\*','CFD Acciones\\CFD ADR\\*','CFD Acciones\\Chile\\*','CFD Acciones\\EEUU\\*','CFD Acciones\\EEUU C\\*','CFD Acciones\\EEUU\\#NIO','CFD Acciones\\EEUU\\#TSLA','CFD Acciones\\EURO\\*','CFD Acciones\\Londres\\*','CFD Acciones\\Tokio\\*','CFD Acciones\\Toronto\\*','CFD Commodities\\*','CFD Commodities\\Futuros 1\\*','CFD Commodities\\Futuros 2\\*','CFD Commodities\\Futuros 3\\*','CFD Commodities\\Spot\\BRENT','CFD Commodities\\Spot\\WTI','CFD Commodities\\Spot\\XAGUSD','CFD Commodities\\Spot\\XAUUSD','CFD Criptomonedas\\*','CFD ETFs\\*','CFD Indices\\*','CFD Indices\\EEUU\\*','CFD Indices\\EU\\*','CFD Indices\\Latam\\*','CFD Indices\\USDX\\*','CFD Indices\\VIX\\*','Forex*','Forex\\*','Forex\\CLP\\*','Forex\\CLP\\USDCLP','Forex\\Majors\\*','Forex\\Majors\\AUDCAD','Forex\\Majors\\AUDJPY','Forex\\Majors\\AUDUSD','Forex\\Majors\\EURAUD','Forex\\Majors\\EURCAD','Forex\\Majors\\EURCHF','Forex\\Majors\\EURGBP','Forex\\Majors\\EURJPY','Forex\\Majors\\EURUSD','Forex\\Majors\\GBPCHF','Forex\\Majors\\GBPJPY','Forex\\Majors\\GBPNZD','Forex\\Majors\\GBPUSD','Forex\\Majors\\NZDUSD','Forex\\Majors\\USDCAD','Forex\\Majors\\USDCHF','Forex\\Majors\\USDCNH','Forex\\Majors\\USDDKK','Forex\\Majors\\USDHKD','Forex\\Majors\\USDJPY','Forex\\Majors\\USDPLN','Forex\\Majors\\USDSGD','Forex\\Majors\\USDTRY','Forex\\Minors\\*','Forex\\Minors\\USDCOP','Forex\\New\\*','Forex\\New\\USDCNH','MarketExecution\\*','Provisorios\\*','START\\*']
paths_grupos_faltantes = [['ETF_SUGO', 'CFD ETFs\\ETF\\ETF_SUGO']]



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
                else:
                    path_grupo is None
                
                
                
print(path_grupos_new)
    

















































# path_grupos_new = list()

# for instrumento, path_instrumento in paths_grupos_faltantes:
#     if path_instrumento in paths_grupos: #busca el path de instrumento, en el path de grupo
#         #print(f"SI1 - {instrumento} - {path_instrumento}")
#         path_grupo = path_instrumento
#     else:
#         path_new_grupo = path_instrumento[:-len(instrumento)]+'*'
#         if path_new_grupo in paths_grupos:
#             #print(f"SI2 - {instrumento} - {path_new_grupo}")
#             path_grupo = path_new_grupo
#         else:
#             path_new_grupo = path_new_grupo[:-2]
#             N = path_new_grupo.find('\\')+1
#             path_new_grupo = path_new_grupo[:N]+'*'
#             if path_new_grupo in paths_grupos:
#                 #print(f"SI3 - {instrumento} - {path_new_grupo}")
#                 path_grupo = path_new_grupo
                
                
#     print(f"{instrumento} : {path_grupo}")
        
    
