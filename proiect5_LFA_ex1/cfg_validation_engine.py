variabile=[]
listadeliste=[]


def citire():
    with open ("cfg_config_file.txt", 'r') as f:
        linii = f.readlines()
        return linii

def prelucrareDate(linii):
    #formare dictionar cu variabile/term
    dict = {}
    for linie in linii:
        dict[linie[0]] = []
        variabile.append(linie[0])
        n = len(linie)
        j = 3
        list = []
        for i in range (n):
            if (linie[i] == '|' or linie[i]=='\n'):
                list = linie[j:i]
                j = i+1
                listadeliste.append(list)
                dict[linie[0]].append(list)
                list = []
    return dict,variabile,listadeliste

def verificare(variabile,listadeliste):
    contor=0
    for i in variabile:
        contor=0
        for j in listadeliste:
            if i in j:
                contor=contor+1
        if contor==0:
            return 0
       
    return contor


linii = citire()
dict = {}
variabile=[]
listadeliste=[]
dict,variabile,listadeliste = prelucrareDate(linii)
print(dict)

print(variabile)

print(listadeliste)

if 'S' not in variabile:
    print("nu e cfg")
elif verificare(variabile,listadeliste)==0:
    print("nu e cfg")
else:
    print("este cfg")

