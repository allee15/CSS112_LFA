from numpy import var


def citire():
    with open ("cfg_config_file.txt", 'r') as f:
        linii = f.readlines()
        return linii

def prelucrareDate(linii):
    #formare dictionar cu variabile/term
    dict = {}
    for linie in linii:

        # linie[0] => prima litera de pe linie
        # daca simbolul e format din mai multe litere nu o sa mai 
        # functioneze schema :)
        dict[linie[0]] = []
        n = len(linie)
        j = 3
        list = []
        for i in range (n):
            if (linie[i] == '|' or linie[i]=='\n'):
                list = linie[j:i]
                j = i+1
                dict[linie[0]].append(list)
                list = []
    return (dict)


def removeNonGenSymbols (dict, i):
    ok = 1
    if len(dict[i])>0:
        for litera in dict[i][-1]:
            if litera>='A' and litera<='Z':
                ok=0
                return ok
    return ok
def cautarePrevious (dict, cheie):
    for key in dict.keys():
        for elem in dict[key]:
            for litera in elem:
                if litera == cheie:
                    return True
    return False
#main
linii = citire()

dict = {}
dict = prelucrareDate(linii)

print (dict)
#useless reduction
scoase = []
dictNou = {}
dictNou['S'] = []
for elem in dict['S']:
    dictNou['S'].append(elem)
for key in dict.keys():
    if key != 'S':
        if (removeNonGenSymbols(dict, key) == 1):
            if cautarePrevious(dict, key) == True:
                dictNou[key] = []
                for elem in dict[key]:
                    dictNou[key].append(elem)
                #print (key, dict[key])
        else:
            scoase.append(key)

#parcurgere dictionar nou pt eliminare variabile useless
print ("--------------------------------")
for key in dictNou.keys():
    n = len(dictNou[key])
    i = 0
    while i < n:
        ok = 1
        for litera in dictNou[key][i]:
            if litera in scoase:
                dictNou[key].pop(i)
                n -= 1
                ok = 0
                break
        if ok == 1:
            i += 1
print (dictNou)



'''


eliminarea productiilor nule 

Luam ca exemplu gramatica din fisierul de configurare 



S->ABAC
A->aA|ε
B->bB|ε
C->c


Observam ca avem doua productii ce trec o variabila 
in ε: acestea sunt A -> ε (de pe linia a doua) si B->ε (de pe linia a treia)



Primul pas al algoritmul ne spune ca, daca avem 
o productie de forma X -> ε, pentru a o elimina trebuie sa gasim productiile care au in partea 
dreapta X (adica il contine pe X)



Deci ce facem prima data e sa gasim acele X-uri pt care exista productii de forma X -> ε. 
Aceste X-uri se numesc variabile nule (o sa le stochez in lista nullable_vars)
'''



def gasireNullableVars():
    nullable_vars = []
    for dict_key in dict.keys():
        if 'ε' in dict[dict_key]:
            nullable_vars.append(dict_key)



    return nullable_vars


nullable_vars = gasireNullableVars()


'''


Acum ca am gasit variabilele, trebuie sa trecem la pasul 2 al algoritmului.


Pasul 2 spune ca, pentru un anumit nullable_var X, trebuie sa inlocuim in fiecare dintre 
production-urile existente X cu ε

Aceste production-urile pe care le obtinem le adaugam intr-o alta lista, si dupa ce 
terminal le adaugam la production-urile initiale

Inca o smecherie de care trebuie tinut cont e ca daca simbolul apare de mai multe 
ori in partea dreapta a production-ului, luam toate combinatiile posibile (o data il luam 
si o data nu il luam pentru fiecare pozitie)


De exemplu daca avem S -> ABAC si noi trebuie sa inlocuim A cu ε, atunci 
noile productii generate sunt BAC, ABC si BC (nu doar BC :) )



Iar pasul 3 e foarte simplu, ne spune sa adaugam productiile rezultate la pasul 2 la productiile 
deja existente in gramatica





Acum sa facem exemplul din fisierul de configurare full 



S->ABAC
A->aA|ε
B->bB|ε
C->c


Pasul 1:
Nullable Vars: A si B (pt ca exista A -> ε si B -> ε)


Pentru A, trecem prin toate productiile posibile si generam productii care in loc de A il pun pe ε


Pt S se vor genera: S->BAC, S->ABC, S->BC
Pt A se vor genera: A->a


Deci am avea urm productii, dupa eliminarea lui A:

S -> ABAC | BAC | ABC | BC 
A -> aA | a
B -> bB | ε
C -> c

Facem acelasi lucru pt B:

Pt S se va genera: S->AAC, S-> AC, S->C
Pt B se va genera B->b

  
Deci am avea urm productii, dupa eliminarea lui B:

S -> ABAC | BAC | ABC | BC | AAC | AC | C
A -> aA | a
B -> bB | b
C -> c

'''

def removeVariableInAllCombinations(str, substr):

    # de exemplu  removeVariableInAllCombinations('ABAC', 'A')
    #  va rezulta in lista ['ABAC', 'BAC', 'ABC', 'BC']


    result = []
    count = str.count(substr)

    nr_posibilitati = 2 ** count

    for current_pos in range(nr_posibilitati + 1):
        current_str_val = ""
        current_layout = bin(current_pos)[2:].zfill(len(str))
        # Trecem prin fiecare pozitie ce contine substr si vedem daca ar trebui pus sau nu
        nr_substr = 0
        for i in range(len(str)):
            if str[i] == substr:
                if current_layout[len(current_layout) - nr_substr - 1] == '1':
                    # Atunci eliminam aparitia
                    pass
                else:
                    # Altfel adaugam litera curenta
                    current_str_val += str[i]
            
                nr_substr += 1
            
            else:
                # Altfel adaugam litera curenta, orice ar fi ea 
                current_str_val += str[i]
        

        result.append(current_str_val)

    return list(set(result))



new_productions = {}


for current_nullable_var in nullable_vars:
    for variable in dict:
        new_productions[variable] = []
        if variable == current_nullable_var:
            # Daca variabila curenta e chiar nullable_var-ul curent 
            # atunci ii eliminam productia care il duce catre epsilon 
            dict[current_nullable_var].remove('ε')

        for current_variable_production in dict[variable]:

            # Pentru fiecare productie, verificam daca contine current_nullable_var
            if current_nullable_var in current_variable_production:
                # Count retine de cate ori se afla current_nullable_var in productia 
                # curenta
                count = current_variable_production.count(current_nullable_var)
        
                new_productions[variable] = new_productions[variable] + removeVariableInAllCombinations(current_variable_production, current_nullable_var)
                # Acum trebuie sa luam toate combinatiile posibile, pe fiecare pozitie pe care 
                # se afla current_nullable_var in current_variable_production, o luam o data 
                # cu eliminare pe pozitia respectiva si o data fara eliminare
        


    # Acum adaugam noile productii la dictionar pt fiecare variabila in parte 
    for variable in dict.keys():
        dict[variable] = list(set(dict[variable] + new_productions[variable]))
    
print ("--------------------------------")
print(dict)