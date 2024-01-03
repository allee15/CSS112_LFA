def creare_matrice (n):
    n = int (n)
    matrix = []
    lungime = 1
    for i in range (n+1):
        ls = [None for i in range(lungime-1)]
        matrix.append(ls)
        lungime +=1
        if lungime == n+1:
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
"""
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
                dict[x].append( (y, litera) )
            else:
                dict[x] = []
                dict[x] .append( (y, litera) )
    return dict
"""
def citire_tranzitii_litere (linii, coloane):
    #creare matrice cu len(noduri) linii si len(sigma) coloane
    matrice = []
    linii = int (linii)
    coloane = int (coloane)
    for i in range (linii):
        ls = [None for j in range (coloane)]
        matrice.append(ls)
    #citire din fisier
    for linie in f:
        linie = linie.split ()
        if linie == ['End']:
            break
        else:
            x = linie[0]
            litera = linie[2]
            y = linie[4]
            #caut pozitiile coresp lui x, y
            for i in range (linii):
                if (noduri[i] == x):
                    break
            for j in range (coloane):
                if letter[j] == litera:
                    break
            for k in range (linii):
                if noduri[k] == y:
                    break
            #adaugare in matrice
            matrice [i][j] = k
    return matrice
#pasul 2
def inlocuire_matrice (matrix):
    n = len (matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            ok = 0
            if noduri[i] in finish:
                ok += 1
            if noduri[j] in finish:
                ok += 1
            if (ok == 2 or ok ==0):
                matrix[i][j] = 0
            else:
                matrix[i][j] = 1
    return matrix
def afisare_matrice (matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print( matrix[i][j], end=" ")
        print()

#j este coloana, i este linia
def verificare_tranzitii (i , j):
    # daca avem (0,1) -> cautam (0,a)=x si (1,a)=y  => (x, y) ? 1
    # (i, j) -> cautam  ( (i, x) , (j, x) ) , daca o gasim ca 1 => matrix[i][j] = 1
    # x este din alfabet
    k=0
    while (k<len(letter) ):
        x = tranzitii[i][k]
        y = tranzitii[j][k]
        #verificare existenta
        if x>y:
            if (matrix[x][y]==1):
                    return 1
        k += 1
    return 0
with open ("dfa_config_file.in",'r') as f:
    #dict = {}
    for i in range (3):
        linie = f.readline()
        linie = linie.split()
        if linie == ["Sigma:"]:
            letter = citire_sigma()
        if linie == ["States:"]:
            noduri, start, finish = citire_states()
        if linie == ["Transitions:"]:
            tranzitii = citire_tranzitii_litere(len(noduri), len(letter))
#citire = citire_tranzitii_litere(len(noduri), len(letter))
""" 
"""
#creare matrice
matrix = creare_matrice(len(noduri))
matrix = inlocuire_matrice(matrix)
#afisare_matrice(matrix)
#parcurgere matrix + cautare 0
n = int (len(matrix))
for i in range(n):
    for j in range(len(matrix[i])):
        if matrix[i][j] == 0:
            #print ()
            matrix[i][j] = verificare_tranzitii (i, j)
#cautare 0-uri ramase + ce noduri vor fi eliminate
listaNoduriFinale = []
for i in range (1,n):
    ok = 0
    for j in range (len(matrix[i])):
        #combinam starile noduri[i]+noduri[j]
        if matrix[i][j] == 0:
            #print (i, j, end=" ")
            listaNoduriFinale.append( (j,i) )
#creare lista frecventa ca sa stim ce noduri s-au unit
frecventaNoduri = [x for x in noduri]
for i in range (len(listaNoduriFinale)):
    frecventaNoduri[listaNoduriFinale[i][0]] = -1
    frecventaNoduri[listaNoduriFinale[i][1]] = -1
#creare lista finala cu nodurile ramase
NoduriFinale = []
for iNod in range (n):
    if frecventaNoduri[iNod] != -1:
        #adaugam indicele
        NoduriFinale.append(iNod)
    else:
        #scoatem din coada, daca mai avem ce
        if len(listaNoduriFinale) != 0:
            x = listaNoduriFinale.pop(0)
            NoduriFinale.append(x)
#listaNoduriFinale == []
#transformare listaNoduri de la indice la nod ( 0->q0)

#identificare tranzitii noi
dictTranzitii = {}
#formare chei
#dictionar cu noile tranzitii
#cheia o reprezinta nodul/setul de noduri
for i in range (len(NoduriFinale)):
    str = ""
    for j in range (len(NoduriFinale[i])):
        str += noduri[NoduriFinale[i][j]]
    dictTranzitii[str] = []


#tranzitii -> dictTranzitii

for stareDFAfinal in NoduriFinale:
    stareDFAfinalKey = ""
    for j in range (len(stareDFAfinal)):
        stareDFAfinalKey += noduri[stareDFAfinal[j]]
    for elem in stareDFAfinal:
        #print("elem={} ".format(elem) )
        for j in range(len(tranzitii[elem])):
            (stare, litera) = (tranzitii[elem][j], letter[j])
            stareCurenta = None
            for stareCurentaCandidat in NoduriFinale:
                if stare in stareCurentaCandidat:
                    # transformare stareCurenta in string  ( (0, 1) -> q0q1 )
                    str = ""
                    for i in range(len(stareCurentaCandidat)):
                        str += noduri[stareCurentaCandidat[i]]
                    stareCurenta = str
                    break
            if (stareCurenta, litera) not in dictTranzitii[stareDFAfinalKey]:
                dictTranzitii[stareDFAfinalKey].append( (stareCurenta, litera) )
            #print((stare, litera) )
            #print (noduri[tranzitii[elem][j]], end= " ")
        print ()

#determinare stare initiala
lungimeNoduriFinale = len(NoduriFinale)
def stareInitiala ():
    for i in range (lungimeNoduriFinale):
        for j in range(len(NoduriFinale[i])):
            if start[0] == noduri[NoduriFinale[i][j]]:
                str = ""
                for j in range (len(NoduriFinale[i])):
                    str += noduri[NoduriFinale[i][j]]
                return str
startFinal = stareInitiala()
#determinare stari finale
finishFinal = []
for i in range (lungimeNoduriFinale):
    for k in range (len(NoduriFinale[i])):
        if noduri[NoduriFinale[i][k]] in finish:
            str = ""
            for j in range (len(NoduriFinale[i])):
                str += noduri[NoduriFinale[i][j]]
            if str not in finishFinal:
                finishFinal.append(str)
#print (finishFinal)
#afisarea noului automat
#noduri
print ("Nodurile sunt:")
for key in dictTranzitii.keys():
    print (key)
print ("Nodul de start este:")
print (startFinal)
print ("Nodurile de finish sunt:")
for stare in finishFinal:
    print (stare)
print ("End")
#alfabet
print("Sigma:")
for litera in letter:
    print(litera)
print ("End")
#transitions
print ("Transitions")
for key in dictTranzitii.keys():
    for pereche in dictTranzitii[key]:
        print(key,  pereche[1], pereche[0],  sep = " , ")
print ("End")