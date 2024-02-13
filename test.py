
#todo - hacer que el path instrumento actualice

mt5 = {'Gasol_Feb24': {'path_instrumento': 'Historicos\\Gasol_Feb24', 'fecha_insercion': '2024-02-02 18:02:45.171'},
       '#META': {'path_instrumento': 'CFD Acciones\\EEUU\\#META', 'fecha_insercion': '2024-02-02 18:02:45.171'}}

#bdd = {'Gasol_Feb24': {'path_instrumento': 'CFD Commodities\\Futuros 3\\Gasol_Feb24'}}
bdd = {'Gasol_Feb24': {'path_instrumento': 'Historicos\\Gasol_Feb24'}}

insert = list()
update = list()
no_update = list()

for instrumento in mt5:
    if instrumento in bdd:
        if mt5[instrumento]['path_instrumento'] != bdd[instrumento]['path_instrumento']:
            update.append(instrumento)
        else:
            no_update.append(instrumento)
    else:
        insert.append(instrumento)
    

print("Insert:", insert)
print("Update:", update)
print("No Update:", no_update)