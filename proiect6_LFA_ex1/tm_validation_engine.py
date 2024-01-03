def citire_sigma ():
    letter = []
    for linie in f:
        linie = linie.split()
        if (linie == ['End']):
            break
        else:
            letter.append(*linie)

    if "'_'" in letter:
        return False
    return True

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
                if linie[1] == ',accept':
                    finish.append(linie[0])
                elif linie[1] == ',start':
                    start.append(linie[0])
                elif (linie[1] == ',accept' and linie[2] == ',start') or (linie[1] == ',start' and linie[2] == ',accept'):
                    finish.append(linie[0])
                    start.append(linie[0])
    return noduri, start, finish

def citire_tranzitii ():
    tranzitii=[]
    for linie in f:
        linie = linie.split ()
        if linie == ['End']:
            break
        else:
            linie = linie.strip()
            linie=linie.split(', ',2)
            if len(linie)!=3:
                return False
            if(linie[0] not in noduri or linie[1] not in letter):
                return False
            if(len(linie[2].split(" "))>2):
                return False
            if(len(linie[2].split(" "))==2 and linie[2].split(" ")[1] not in "LR" ) :
                return False
            if(linie[2].split(" ")[0] not in noduri):
                return False
            tranzitii.append(linie)
    return True

def citire_tape():
    tape=[]
    for linie in f:
        linie = linie.split ()
        if linie == ['End']:
            break
        else:
            linie = linie.strip()
            tape.append(linie)
    if "'_'" not in tape:
        return False
    return True

ok=1
with open ("tm_config_file.txt",'r') as f:
        linie = f.readline()
        linie = linie.split()
        if linie == ["Sigma:"]:
            if citire_sigma() == False:
                ok=0
        if linie == ["States:"]:
            noduri, start, finish = citire_states()
        if linie == ["Transitions:"]:
            if citire_tranzitii()==False:
                ok=0
        if linie == ["Tape:"]:
            if citire_tape() == False:
                ok=0

        if len(start)!=1:
            ok=0
        if( len(finish)!=1):
            ok=0
if ok==1:
    print("este tm")
else:
    print("nu e")
   

