def creare_matrice (n):
    n = int (n)
    matrix = []
    for i in range (n):
        ls = [None for i in range(n)]
        matrix.append(ls)
    return matrix

def citire_sigma ():
    letter = []
    for linie in f:
        linie = linie.split()
        if (linie == ['End']):
            break
        else:
            letter.append(*linie)
    return letter
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
            if (x in dict.keys()):
                for elem in dict[x]:
                    for pereche in elem:
                        if pereche == y:
                            return -1
                dict[x].append( (y, litera) )
            else:
                dict[x] = []
                dict[x] .append( (y, litera) )
    return dict

def valid_cuvant():
    cuvant = input("cuvant=")
    n = len(cuvant)
    st = start[0]
    cnt = 0
    if cuvant[n-1] == '\n':
       n -=  1
    for i in range (n):
       for elem in dict[st]:
            if elem[1] == cuvant[i]:
                st = elem[0]
                cnt += 1
    if cnt == n:
        return 1
    else:
        return -1
#init ok
ok = 1
with open ("dfa_config_file.in",'r') as f:
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
   
    if valid_cuvant() == -1:
        print ("Cuvant nevalid")
    else:
        print ("Cuvant valid")


