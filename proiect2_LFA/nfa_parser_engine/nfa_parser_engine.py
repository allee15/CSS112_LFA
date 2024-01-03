#citirea literelor
def citire_sigma ():
    letter = []
    for linie in f:
        linie = linie.split()
        if (linie == ['End']):
            break
        else:
            letter.append(*linie)
    return letter
#citire stari (q0,q1....
def citire_states ():
    noduri = []
    finish = []
    start = []
    for linie in f:
        linie = linie.split()
        if (linie == ['End']):
            break
        else:
            noduri.append(linie[0])
            if len(linie) >= 2:
                # nod de finish
                if linie[1] == ',F':
                    finish.append(linie[0])
                elif linie[1] == ',S':
                    start.append(linie[0])
                elif (linie[1] == ',F' and linie[2] == ',S') or (linie[1] == ',S' and linie[2] == ',F'):
                    finish.append(linie[0])
                    start.append(linie[0])
    return noduri, start, finish
def citire_tranzitii ():
    dict = {}
    for linie in f:
        linie = linie.split ()
        if linie == ['End']:
            break
        else:
            x = linie[0]
            litera = linie[2]
            y = linie[4]
            #daca a fost deja introdus ca si cheie, ii adaugam inca un elem
            if (x in dict.keys()):
                dict[x].append( (y, litera) )
            else:
                dict[x] = []
                dict[x] .append( (y, litera) )
    return dict
def verif_trans ():
    for key in dict.keys():
        if key not in noduri:
            return -1
        else:
            for elem in dict[key]:
                if elem[0] not in noduri:
                    return -1
                if elem[1] not in letter:
                    return -1
    return 1          

with open ("nfa_config_file.in",'r') as f:
    dict = {}
    for i in range (3):
        linie = f.readline()
        linie = linie.split()
        if linie == ["Sigma:"]:
            letter = citire_sigma()
        if linie == ["States:"]:
            noduri, start, finish = citire_states()
        if linie == ["Transitions:"]:
            dict = citire_tranzitii()

    #validare NFA
    if verif_trans() == 1:
        print ("AFN valid")
    else:
        print("AFN-ul nu este valid")
