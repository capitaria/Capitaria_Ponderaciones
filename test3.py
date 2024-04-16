path_grupo = 'CFD Acciones\EEUU\*'
lista = 'CFD*'

#print(path_grupo[:path_grupo.rfind("\\")+1]+'*',' = ',lista)
print(path_grupo[:path_grupo.find('*')]+'*')

# path_grupo = [CFD Acciones\EEUU\#AAPL, CFD Acciones\EEUU\*]
# lista = [CFD Acciones\EEUU\#AAPL, CFD Acciones\EEUU\*, CDF*]
if ({path_grupo} == {lista} or # [1: CFD Acciones\EEUU\#AAPL = CFD Acciones\EEUU\*] / [2: CFD Acciones\EEUU\* = CFD Acciones\EEUU\*] / [3: CFD Acciones\EEUU\* = CDF*]
    {path_grupo[:path_grupo.find('*')]+'*'} in {lista} or
    {path_grupo[:path_grupo.find(' ')]+'*'} == {lista} or # [1: CFD* en CFD Acciones\EEUU\*] / [3: CFD* = CDF*]
    {path_grupo[:path_grupo.rfind('\\')+1]+'*'} == {lista} or # [1: CFD Acciones\EEUU\* = CFD Acciones\EEUU\*]
    {path_grupo[:path_grupo.rfind('\\')+1]} == {lista} or
    {path_grupo[:path_grupo[:path_grupo.rfind('\\')].rfind('\\')]+'*'} == {lista}):
    print("\n\nSI")
else:
    print("\n\nNO")    