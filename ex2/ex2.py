#grupa 144, echipa formata din Aldea Alexia, Bucur Denisa, Brustur Erwin

def citire_sigma(): #subprogram pentru citirea literelor si formarea listei de litere
    letter = []
    for linie in f:
        linie = linie.split()
        if (linie == ['End']): 
        #daca dam de End => am terminat de citit multimea sigma si ne intoarcem in main pentru a citi si restul fisierului
            break
        else:
            letter.append(*linie) #adaugam litera in lista de litere

    return letter #returnam lista de litere


def citire_states(): #subprogram pentru citirea starilor/nodurilor si formarea listei de noduri, a celei de accept si de reject
    noduri = []
    accept = []
    reject = []

    for linie in f:
        linie = linie.split()
        if (linie ==['End']):
        #daca dam de End => am terminat de citit multimea states si ne intoarcem in main pentru a citi si restul fisierului
            break
        else:
            if linie != 'accept' and linie != 'reject':
                #daca nu este stare de accept sau de reject, o adaugam la lista de noduri
                noduri.append(*linie)
            elif linie == 'accept':
                accept.append(*linie) #daca e stare de accept, o adaugam la lista de accept
            elif linie == 'reject':
                reject.append(*linie) #analog pt reject
    return noduri, accept, reject #returnam cele 3 liste formate


def citire_tranzitii(): #subprogram pentru citirea tranzitiilor si formarea listei de tranzitii
    tranzitii = []
    linie=f.readline()
    while linie:
        linie=linie.split()
        if linie[0] not in noduri or linie[3] not in noduri: #pe linie de 0 si linie de 3 avem starile ( A x x B x x R)
            break #daca acestea nu apar in lista de noduri, iesim deoarece nu este tranzitie valida
        elif linie[1] not in tape or linie[2] not in tape or linie[4] not in tape or linie[5] not in tape: 
            #in linie[1], linie[2], linie[4] si linie[5] avem literele din cele 2 stari, din cele 2 tape-uri
            #daca acestea nu se regasesc in lista de tape data in input, din nou =>tranzitie invalida
            break
        elif linie[6] not in 'LR': #linie[6] va avea mereu una din literele L sau R, indicand sensul de mers pt head
            #daca este altceva scris in linie[6], nu este valid
            break
        elif linie=='End':
            break #daca dam de End=> am terminat de citit tranzitiile
        tranzitii.append(linie) #adaugam tranzitia citita la lista de tranzitii
        #daca am ajuns pana aici, inseamna ca tranzitia curenta este valida
        linie=f.readline() #citim linie noua din fisier
    return tranzitii #returnam lista formata cu listele de tranzitii

def citire_tape(): #citim si ne formam lista de tape
    tape = []
    for linie in f:
        linie = linie.split()
        if linie == ['End']:
            break #daca dam de End=> am terminat de citit tape-ul
        else:
            tape.append(*linie) #altfel adaugam ce am citit la lista de tape

    return tape #returnam lista de tape


def citire_start(): #aici citim si salvam startul, ca sa stim  de unde pleaca head-ul
    start = []
    for linie in f:
        linie = linie.split()
        if linie == ['End']:
            break
        else:
            start.append(*linie)
    return start


def verificare(letter, tape): #subprogram pentru verificarea faptului ca toate literele din sigma apar si in tape+ blankspace
    ok = 1
    for i in letter:
        if i not in tape:
            ok = 0
    return ok

def verificare_string(simulator): #verificam daca literele din string-ul citit apar in lista de sigma si ca mai avem in plus maxim 
    #caracterul blankspace, pe care l-am notat cu _
    for i in simulator:
        if i not in letter and i !='_':
            return 0
    return 1

letter = []
noduri = []
start = []
accept = []
reject = []
tranzitii = []
tape = []

#citim din fisierul input.txt, inputul unui TM, linie cu linie
#fisierul va fi de tipul:
#Nume componenta TM:
#--atributele--
#End
#inputul acesta este similar cu cel folosit pentru validarea unui DFA/NFA
with open("input.txt", 'r') as f:
    linie = f.readline() #citim linie cu linie
    cuvant='' #aici retinem stringul pe care il vom folosi, mai tarziu, in simulator 
    while linie: #cat timp avem linii de citit in fisier
        linie = linie.split() 
        #dam split elementelor de pe linia curenta si verificam ce componenta a TM-ului citim, apoi ne vom ajuta de subprograme 
        #pentru a citi fiecare componenta si pentru a-i stoca atributele undeva
        if linie == ["States:"]: #citim starile, pe cele normale le salvam in lista de noduri, unde vom avea toate nodurile din TM
            #starea de accept o vom stoca intr-o lista separata, similar pt cea de reject
            noduri, accept, reject = citire_states()
        if linie == ["Sigma:"]:#citim sigma, adica literele din TM
            letter = citire_sigma() #salvam literele intr-o lista de letters
        if linie == ["Start:"]:#avem o clauza separata pt nodul de start, ca sa stim de unde pornim
            start = citire_start()
        if linie == ["Tape:"]: #ne cream o lista pt tape-ul nostru
            tape = citire_tape()
        if linie == ["Transitions:"]:#cream o lista de liste, pt fiecare tranzitie practic o matrice de tranzitii, in python
            #de asemenea, in inputul nostru, interpretam tranzitiile pt TM cu 1 head si 2 tape-uri, astfel:
            #(sa luam pt prima linie din input-> A x x B x x R)
            #primul element (A) de pe linie reprezinta nodul de unde pornim tranzitia
            #apoi, urmatorul element (x) reprezinta litera nodului A din tape-ul 1
            #urmatorul x reprezinta litera nodului A din tape-ul 2
            #urmeaza B, adica nodul unde vrem sa ne deplasam
            #apoi urmatorul x reprezinta litera nodului B din tape-ul 1
            #si ultimul x reprezinta litera nodului B din tape-ul 2
            #R-ul final (poate fi si L) reprezinta directia catre care se va deplasa head-ul in tape
            tranzitii = citire_tranzitii()
        if linie==["Input:"]: #retinem cuvantul pe care il vom valida in simulator
            linie = f.readline()
            cuvant=linie
            break
        linie = f.readline() #citim si restul liniilor, pe rand
ok=1 #variabila globala, presupunem ca inputul dat este un TM si cautam neregulile
#daca ok ramane 1 pana la final, inseamna ca inputul dat formeaza un TM
if len(start)!=1 or start[0] not in noduri: #nu putem avea mai multe start-uri, iar nodul de start trebuie sa apara si in lista de noduri
    ok=0 #daca una din aceste conditii este incalcata ok isi schimba valoarea pentru a afisa la final mesaj corespunzator
if '_' in letter or '_' not in tape:
    ok=0
if verificare(letter,tape)==0: #vrem sa verificam ca toate literele din input apar in tape
    ok=0
if ok==0:
    print("Nu e turing machine")
else:
    print("Este turing machine")
    simulator = cuvant #incepem validarea cuvantului dat in input
    if verificare_string == 0: #daca fiecare litera a acestuia nu se regaseste in lista de letters a TM-ului nostru, cuvantul este invalid 
        print("String neacceptat")
    else: #in caz contrar, cuvantul poate fi valid si il verificam
        curent_state = start[0] #vrem mereu sa retinem in ce  nod ne aflam (unde este head-ul); initial, acesta este pe start
        tape_track1 = [] #ne cream 2 liste de track-uri, pentru a ne forma cele 2 tape-uri
        tape_track2 = []
        j = 0
        t = 0
        #formam intai primul tape
        for lit in simulator: #parcurgem literele cuvantului dat in input
            for i in range(len(tranzitii)): #parcurgem fiecare lista de tranzitii
                if tranzitii[i][0] == curent_state and tranzitii[i][1] == lit: 
                    #daca am ajuns la tranzitia corespunzatoare curent_state-ului nostru, iar litera curenta apare in tranzitia curenta,
                    #aflam in ce directie trebuie sa mergem: right sau left in tape-ul nostru
                    if tranzitii[i][6] == 'R': #daca trebuie sa mergem la dreapta, doar adaugam litera la tape-ul nostru 
                        #(append o insereaza in dreapta oricum) si crestem j, un contor ca sa stim nde ne aflam in tape1
                        tape_track1.append(tranzitii[i][4])
                        j += 1
                    else: #altfel, mergem in partea stanga si suprascriem litera la pozitia j in tape
                        tape_track1[j] = lit
                        j -= 1 #j scade pt ca noi practic ne-am intors prin aceasta suprascriere
                    curent_state = tranzitii[i][3] #retinem si in ce nod ne-am mutat acum
                    if (curent_state == 'reject'): #daca am dat de nodul reject, inseamna ca string-ul dat in input nu este bun
                        print("Stringul nu e acceptat")
                        break
                    break

        if curent_state == 'accept': #daca ajunge in nodul de accept, formam tape-ul 2 similar ca la tape-ul 1
            curent_state = start[0]
            j=0
            for lit in simulator:
                for i in range(len(tranzitii)):
                    if tranzitii[i][0] == curent_state and tranzitii[i][2] == lit:
                        if tranzitii[i][6] == 'R':
                            tape_track2.append(tranzitii[i][5])
                            j += 1
                        else:
                            tape_track2[j] = lit
                            j -= 1
                        curent_state = tranzitii[i][3]
                        if (curent_state == 'reject'):#daca ajungem in nodul de reject => string-ul dat nu este valid
                            print("nu e bun")
                            break
                        break
            if curent_state == 'accept': #daca ajungem in starea de accept =>string-ul dat este valid si afisam mesaj corespunzator
                print("String acceptat")
                