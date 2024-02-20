BDD = {'CAC_Feb24': {'path_instrumento': 'Historicos\\CAC_Feb24', 'path_grupo': 'CFD Indices\\EU\\*'},
       'CAC_Mar24': {'path_instrumento': 'CFD Indices\\EU\\CAC_Mar24', 'path_grupo': 'Provisorios\\*'},
       'CafeC_May24': {'path_instrumento': 'CFD Commodities\\Futuros 3\\CafeC_May24', 'path_grupo': 'Provisorios\\*'},
       'ETF_IBIT': {'path_instrumento': 'CFD ETFs\\ETF\\ETF_IBIT', 'path_grupo': 'Provisorios\\*'}, 
       'ETF_IEF': {'path_instrumento': 'CFD ETFs\\ETF\\ETF_IEF', 'path_grupo': 'Provisorios\\*'}, 
       'IBEX_Feb24': {'path_instrumento': 'Historicos\\IBEX_Feb24', 'path_grupo': 'CFD Indices\\EU\\*'}, 
       'IBEX_Mar24': {'path_instrumento': 'CFD Indices\\EU\\IBEX_Mar24', 'path_grupo': 'Provisorios\\*'}, 
       '#NVTA': {'path_instrumento': 'Historicos\\#NVTA', 'path_grupo': 'CFD Acciones\\EEUU\\*'}, 
       '#SMCI': {'path_instrumento': 'CFD Acciones\\EEUU\\#SMCI', 'path_grupo': 'Provisorios\\*'}, 
       'WTI_Abr24': {'path_instrumento': 'CFD Commodities\\Futuros 3\\WTI_Abr24', 'path_grupo': 'Provisorios\\*'},
       'ETF_EEM': {'path_instrumento': 'CFD ETFs\\ETF\\ETF_EEM', 'path_grupo': 'CFD ETFs\\*'},
       'WTI_Jul23': {'path_instrumento': 'Historicos\\WTI_Jul23', 'path_grupo': '*'}}


for instrumento in BDD:
    print(instrumento)
    print(BDD[instrumento]['path_instrumento'][0:BDD[instrumento]['path_instrumento'].find("\\")])
    print(BDD[instrumento]['path_grupo'][0:BDD[instrumento]['path_grupo'].find("\\")])
    if BDD[instrumento]['path_instrumento'][0:BDD[instrumento]['path_instrumento'].find("\\")] == BDD[instrumento]['path_grupo'][0:BDD[instrumento]['path_grupo'].find("\\")]:
        print('NO UPDATE: ',instrumento)
    elif BDD[instrumento]['path_instrumento'][0:BDD[instrumento]['path_instrumento'].find("\\")] == 'Historicos' and BDD[instrumento]['path_grupo'] == '*': 
        print('HISTORICO: ', instrumento)
    else:
        print('UPDATE: ', instrumento)
    
    print("\n")