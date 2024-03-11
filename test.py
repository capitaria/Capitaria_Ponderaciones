instrumentos_mt5 = {'#ADBE': {'path_instrumento': 'CFD Acciones\\EEUU\\#ADBE', 'fecha_insercion': '2024-03-08 23:45:31.472'}, 'CENCOSUD': {'path_instrumento': 'Provisorios\\CENCOSUD', 'fecha_insercion': '2024-03-08 23:45:31.472'}, 'FALABELLA': {'path_instrumento': 'Provisorios\\FALABELLA', 'fecha_insercion': '2024-03-08 23:45:31.472'}, 'MALLPLAZA': {'path_instrumento': 'Provisorios\\MALLPLAZA', 'fecha_insercion': '2024-03-08 23:45:31.472'}, 'RIPLEY': {'path_instrumento': 'Provisorios\\RIPLEY', 'fecha_insercion': '2024-03-08 23:45:31.472'}, '#VLO': {'path_instrumento': 'CFD Acciones\\EEUU\\#VLO', 'fecha_insercion': '2024-03-08 23:45:31.472'}}
instrumentos_path = {'#ADBE': {'path_instrumento': 'CFD Acciones\\EEUU\\#ADBE', 'path_grupo': None}, 'CENCOSUD': {'path_instrumento': 'Provisorios\\CENCOSUD', 'path_grupo': None}, 'FALABELLA': {'path_instrumento': 'Provisorios\\FALABELLA', 'path_grupo': None}, 'MALLPLAZA': {'path_instrumento': 'Provisorios\\MALLPLAZA', 'path_grupo': None}, 'RIPLEY': {'path_instrumento': 'Provisorios\\RIPLEY', 'path_grupo': None}, '#VLO': {'path_instrumento': 'CFD Acciones\\EEUU\\#VLO', 'path_grupo': None}}

insert = list()
update = list()
no_update = list()

for instrumento in instrumentos_mt5: # Muestra los "instrumentos de MT5"
    if instrumento in instrumentos_path: # Si el "instrumento de MT5" esta en los "instrumentos de BDD (ponderaciones path)"
        if instrumentos_mt5[instrumento]['path_instrumento'] != instrumentos_path[instrumento]['path_instrumento']: # Si el "Path Instrumento" de MT5 es distinto al "Path Instrumento" de la BDD
            update.append([instrumento,instrumentos_mt5[instrumento]['path_instrumento']])
        # elif instrumentos_path[instrumento]['path_instrumento'][0:instrumentos_path[instrumento]['path_instrumento'].find("\\")] == 'Provisorios' and instrumentos_path[instrumento]['path_grupo'] is None:
        #     update.append([instrumento,instrumentos_path[instrumento]['path_instrumento']])
        elif instrumentos_path[instrumento]['path_instrumento'][0:instrumentos_path[instrumento]['path_instrumento'].find("\\")] == 'Historicos' and instrumentos_path[instrumento]['path_grupo'] == '*': # Si el grupo instrumento "inicia en Historico" y el grupo path tiene "*", no actualiza 
            no_update.append([instrumento,instrumentos_path[instrumento]['path_instrumento']])
        elif instrumentos_path[instrumento]['path_grupo'] is not None: #! si el path grupo NO viene vacio
            if instrumentos_path[instrumento]['path_instrumento'][0:instrumentos_path[instrumento]['path_instrumento'].find("\\")] != instrumentos_path[instrumento]['path_grupo'][0:instrumentos_path[instrumento]['path_grupo'].find("\\")]: # Si el "inicio del Path Instrumento" es distinto al "Inicio de Grupo Path"
                update.append([instrumento,instrumentos_path[instrumento]['path_instrumento']])
        else: # Si no es distinto, entonces no actualiza
            no_update.append([instrumento,instrumentos_mt5[instrumento]['path_instrumento']])
    else: # Si el "Instrumento MT5" no esta en "Instrumento BDD" entonces lo inserta
        insert.append([instrumento,instrumentos_mt5[instrumento]['path_instrumento'],instrumentos_mt5[instrumento]['fecha_insercion']])



print(f"\nInsert ({len(insert)}): {[x[0] for x in insert]}")
print(f"\nUpdate ({len(update)}): {[x[0] for x in update]}")
print(f"\nNO Update ({len(no_update)}): {[x[0] for x in no_update]}")