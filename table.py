def exract_variable(hypothese):
    e = [x for x in hypothese.replace("(", "").replace(")", "").replace('v', ' ').replace('^', ' ').replace('->', ' ').replace('<=>', ' ').split()]
    for i in range(len(e)):
        pivot = e[i]
        for j in range(i + 1, len(e)):
            if e[j] == pivot: e[j] = ""
    variables = [element for element in e if element != ""]

    for i, t in enumerate(variables): # ajouter une variable sans ! s'il n'existe pas encore
        if t[0] == "!": # s'il existe un variable avec !
            pivot, isZero = t, True
            for j in range(len(variables)):
                if j != i:
                    if pivot == "!"+variables[j]:
                        isZero = False
                        break
                    else: isZero = True
            if isZero: variables.insert(i, variables[i].replace("!", ""))
    variables.sort() # trier la sortie
    return variables

def table_des_variables(variables):
    n, variable_positive = 0, [] # variable_positive Variable sans !
    for i in range(len(variables)):
        if variables[i][0] != "!":
            variable_positive.append(variables[i])
            n += 1
    variable_negative = [variables[i] for i in range(len(variables)) if variables[i][0] == "!"] # Variable avec !
    length = 2 ** n # nombre de ligne de la table de verité
    A, B = [], [] # B est la matrice contenant les binaire du variable_positive. et A pour le variable_negative
    for i in range(n):
        zero = length // (2 ** (i + 1)) # nombre d'apparition de "0" successivement avant "1"
        a, tmp, temp = [0], [], [] # la variable "a" c'est pour verifier assurer les succetion de "0" et "1"
        for j in range(length):
            if (j == 0 or a[j] > a[j - 1] or a[j] == 0):
                a.append(a[j] + 1)
                if a[j] == zero: # si le nombre d'apparition est atteint
                    a[j + 1] = a[j] - 1
                    tmp.append(1)
                    continue
                tmp.append(0)
            else:
                tmp.append(1)
                a.append(a[j] - 1)
        B.append(tmp)
        if "!"+variable_positive[i] in variable_negative:
            for j in range(len(B[0])):
                if B[i][j] == 0: temp.append(1)
                else: temp.append(0)
            A.append(temp)
    B.extend(A) # assembler A dans B
    # a_transposed = [[B[j][i] for j in range(len(B))] for i in range(len(B[0]))]
    variable_positive.extend(variable_negative)
    return B, variable_positive

def extract_subformulas(formula): # c'est pour extraire dans une liste les terms dans des parenthese. exemple: (p -> (r v (s ^ q))) output : [(s ^ q), (r v (s ^ q)), (p -> (r v (s ^ q)))]
    subformulas = set()
    stack, current_subformula = [], ""
    for char in formula:
        if char == '(':
            if current_subformula: stack.append(current_subformula)
            current_subformula = char
        elif char == ')':
            current_subformula += char
            subformulas.add(current_subformula)
            if stack: current_subformula = stack.pop() + current_subformula
            else:
                subformulas.add(current_subformula)
                current_subformula = ""
        elif char in ['v', 'p', 'q', 'r', '!', '-', '>', '<', '=', ' ']:
            current_subformula += char
        else:
            current_subformula += char
    if current_subformula: subformulas.add(current_subformula)
    return sorted(subformulas, key=len)

def implique(a, b): return 0 if a == 1 and b == 0 else 1
def etLogique(a, b): return a * b
def ouLogique(a, b): return 1 if a == 1 or b == 1 else 0
def equivalance(a, b): return 1 if a == b else 0 

# supposons qu'on a (p -> q), le but de cette fonction est d'extraire les variable a,b,r telque a = "p" et b = "q" et r = "->". l'extraction se fait par tour
def find_abr(hyp, a = "", b = "", r = "", isA = True, isB = False): 
    for h in hyp:
        if h not in ["v","^","-",">","<","="]:
            if isA: a += h
            if isB: b += h
        else: # si l'une des operateurs est detecté, fin pour a et c'est le tour de b
            r += h
            isA = False
            isB = True
    return a, b, r

def find_valeur_ab(a, b, B, variable_positive, sub_variable): # trouver les valeurs binaire correspondant à (a et b). a et/ou b peut etre des indice
    va, vb = [], []
    if b == "": # si b n'existe pas
        if len(sub_variable) > 0:
            if a[0] == "!":
                a = a.replace("!", "") # enlever la negation s'il y en a, pour pouvoir le convertir en int()
                for j in range(len(B[0])): # extraire les valeurs de va
                    if sub_variable[int(a)][j] == 0: va.append(1)
                    else: va.append(0)
            else: va = [sub_variable[int(a)][j] for j in range(len(B[0]))]
            return va, vb
    for i, v in enumerate(variable_positive):
        if v == a:
            va = [B[i][j] for j in range(len(B[i]))]
        if v == b and b != "":
            vb = [B[i][j] for j in range(len(B[i]))]
    return va, vb

def combiner(B, va, vb, a, b, r, pred): # pred est une liste qui contient les valeurs des solutions precedent
    solution = []
    if len(va) == 0: va = pred[int(a)] # si va est vide, remplier par l'un de des solutions precedent, correspondent à l'indice de "a"
    if len(vb) == 0: vb = pred[int(b)] # pareil pour vb
    for i in range(len(B[0])):
        if r == "v": operation = ouLogique(va[i],vb[i])
        if r == "^": operation = etLogique(va[i],vb[i])
        if r == "->": operation = implique(va[i],vb[i])
        if r == "<=>": operation = equivalance(va[i],vb[i])
        solution.append(operation)
    return solution

def solve(hypothese):
    variables = exract_variable(hypothese)
    B, variable_positive = table_des_variables(variables)
    subformul = extract_subformulas(hypothese)
    subformul[len(subformul)-1] = hypothese # pour s'assurer que la derniere indice est l'hypothese de depart
    sub = subformul.copy()
    temp = [f"{i}" for i in range(len(subformul))] # temp contient l'indice (que a et b pouront emprunter)
    solution, sub_variable, i, j = [], [], 0, 0

    while i < len(subformul):
        sub[i] = sub[i].replace("(", "").replace(")", "").replace(" ", "")
        a, b, r = find_abr(sub[i])
        va, vb = find_valeur_ab(a, b, B, variable_positive, sub_variable)
        if a != "" and b != "": solution = combiner(B, va, vb, a, b, r, sub_variable)
        else: solution = va
        sub_variable.append(solution)
        i += 1
        for j in range(i, len(subformul)): 
            sub[j] = sub[j].replace("(", "").replace(")", "").replace(" ", "")
            if subformul[i-1] in subformul[j] and subformul[i-1] != subformul[j]: # si le subformul courent est present dans les autres
                sub[j] = sub[j].replace(sub[i-1], temp[i-1]) # remplacez-le par une indice
        print(sub)

    B.extend(sub_variable)
    variable_positive.extend(subformul)
    print(variable_positive)
    for i in range(len(B[0])): # affichage
        print(" | ".join(str(B[j][i]) for j in range(len(variable_positive))))

if __name__ == "__main__":
    hypothese = "p <=> (!q v (p -> !r))"
    solve(hypothese)