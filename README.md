```
def exract_variable(hypothese):
    e = [x for x in hypothese.replace("(", "").replace(")", "").replace('v', ' ').replace('^', ' ').replace('->', ' ').replace('<=>', ' ').split()]
    for i in range(len(e)):
        pivot = e[i]
        for j in range(i + 1, len(e)):
            if e[j] == pivot: e[j] = ""
    variables = [element for element in e if element != ""]
```
# But : Extraire toutes les variables (lettres) présentes dans une hypothèse logique.
- Étape 1 : Retirer les opérateurs logiques et parenthèses, et créer une liste des variables.
- Étape 2 : Supprimer les doublons dans la liste de variables.
```
    for i, t in enumerate(variables): 
        if t[0] == "!": 
            pivot, isZero = t, True
            for j in range(len(variables)):
                if j != i:
                    if pivot == "!"+variables[j]:
                        isZero = False
                        break
                    else: isZero = True
            if isZero: variables.insert(i, variables[i].replace("!", ""))
    variables.sort() 
    return variables
```
- Étape 3 : Vérifier si une variable avec une négation (!) existe. Si c'est le cas, ajouter sa version positive si elle n'est pas déjà présente.
- Étape 4 : Trier les variables et les renvoyer.

```
def table_des_variables(variables):
    n, variable_positive = 0, [] 
    for i in range(len(variables)):
        if variables[i][0] != "!":
            variable_positive.append(variables[i])
            n += 1
```

# But : Générer la table de vérité pour les variables extraites.
variable_positive : Liste des variables sans négation (!).

```
    variable_negative = [variables[i] for i in range(len(variables)) if variables[i][0] == "!"]
    length = 2 ** n 
    A, B = [], [] 
    for i in range(n):
        zero = length // (2 ** (i + 1))
        a, tmp, temp = [0], [], []
        for j in range(length):
            if (j == 0 or a[j] > a[j - 1] or a[j] == 0):
                a.append(a[j] + 1)
                if a[j] == zero:
                    a[j + 1] = a[j] - 1
                    tmp.append(1)
                    continue
                tmp.append(0)
            else:
                tmp.append(1)
                a.append(a[j] - 1)
        B.append(tmp)
```

# Boucles : Générer les valeurs binaires pour chaque variable positive (1 ou 0) pour chaque ligne de la table.
A et B : Matrices contenant les valeurs pour les variables positives et négatives.

```
      if "!"+variable_positive[i] in variable_negative:
            for j in range(len(B[0])):
                if B[i][j] == 0: temp.append(1)
                else: temp.append(0)
            A.append(temp)
    B.extend(A)
    variable_positive.extend(variable_negative)
    return B, variable_positive
```
# Gestion des négations : Si une variable positive a une version négative, inverser les valeurs binaires correspondantes.

```
def extract_subformulas(formula):
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
```
# But : Extraire toutes les sous-formules présentes dans une formule entre parenthèses.
# stack : Utilisé pour gérer l'imbrication des parenthèses et collecter les sous-formules complètes.

```
def find_abr(hyp, a = "", b = "", r = "", isA = True, isB = False):
    for h in hyp:
        if h not in ["v","^","-",">","<","="]:
            if isA: a += h
            if isB: b += h
        else:
            r += h
            isA = False
            isB = True
    return a, b, r
```

# But : Extraire les deux opérandes (a, b) et l'opérateur (r) d'une sous-formule.

```
def find_valeur_ab(a, b, B, variable_positive, sub_variable):
    va, vb = [], []
    if b == "":
        if len(sub_variable) > 0:
            if a[0] == "!":
                a = a.replace("!", "")
                for j in range(len(B[0])):
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
```

# But : Trouver les valeurs binaires pour les opérandes a et b à partir de la table de vérité.

```

```
