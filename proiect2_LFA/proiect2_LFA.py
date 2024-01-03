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

def validare_cuvant (cuvant):
    queue = []
    #pornim cu nodul de start
    queue.append(start)
    for litera in cuvant:
     #   print (u)
        for lista in queue:
            if len(lista) == len(queue[0]):
                # scoatem primul elem din coada
                list = [x for x in queue[0]]
                # scoatem ultimul elem din capul cozii
                u = list[-1]
                for pereche in dict[u]:
                    if pereche[1] == litera:
                        list.append(pereche[0])
                        queue.append(list)
                        list = [x for x in queue[0]]
                        #print (pereche)

                queue.pop(0)
    #indice de verificare
    ok=0
    for elem in queue:
        #lungime = len(cuvant)+1
        if (len(elem) == len(cuvant)+1 and elem[-1] in finish) :
            ok=1
    if ok==1:
        return 1
    else:
        return 0
    return queue           

def conversie_afd(dict,start, finish,letter,noduri):
    qprim=[]
    d1={}
    print(dict)
    qprim.append((start[0]))
    i=0
    while i<=len(qprim)-1:
        d1[qprim[i]]=[]
        for j in range(len(letter)):
            v=[]
            for y in qprim[i]:
                for cheie in dict:
                    for perechi in dict[cheie]:
                        if perechi[1]==letter[j]:
                            v.append(perechi[0])
                v=list(set(v))
                v.sort()
                d1[qprim[i]].append( (v,letter[j]) )
            if v not in qprim:
                qprim.append(v)
        print(d1)
        i+=1
    return d1,qprim

with open ("ceva.in",'r') as f:
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
        #incepere validare cuvant
        if validare_cuvant("aab") == 1:
            print ("Cuvant valid")
        else:
            print ("Cuvantul NU este valid")

