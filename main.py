import math
from prettytable import PrettyTable  # type: ignore

poczki = open("poczki.txt", "r")
trenerzy = poczki.readline().split(",")

table_header_1 = trenerzy[0]+" <-> "+trenerzy[1]
table_header_2 = trenerzy[1]+" <-> "+trenerzy[2].replace("\n","")
table_header_3 = trenerzy[2].replace("\n","")+" <-> "+trenerzy[0]

tablica_final = PrettyTable(["",table_header_1,table_header_2,table_header_3])

suma_12 = 0
suma_23 = 0
suma_31 = 0
i = 0
for x in poczki:
    i += 1
    array = x.split(",")
    tr_1 = int(array[1])
    tr_2 = int(array[2])
    tr_3 = int(array[3])
    suma = tr_1 + tr_2 + tr_3
    wym_23 = math.floor((suma/2 - tr_1))
    wym_31 = math.floor((suma/2 - tr_2))
    if suma%2==0:
        wym_12 = math.floor((suma/2 - tr_3))
        
    if suma%2==1:
        wym_12 = math.ceil((suma/2 - tr_3))        
        
    suma_12 += wym_12
    suma_23 += wym_23
    suma_31 += wym_31
    
    tablica_final.add_row([array[0],wym_12,wym_23,wym_31], divider=True)    

tablica_final.add_row(["RAZEM",suma_12,suma_23,suma_31]) 
print(tablica_final)        
poczki.close()