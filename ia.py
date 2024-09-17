def transposed(Mat):
    t = []
    for i in range(len(Mat[0])):
        tmp = []
        for j in range(len(Mat)):
            tmp.append(Mat[j][i])
        t.append(tmp)
    # return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]
    return t

def determinant(Mat):
    return (Mat[0][0] * Mat[1][1]) - (Mat[0][1] * Mat[1][0])

def produit(A, B):
    ligne = len(A)
    colonne = len(B[0])
    c = len(B)
    p = []
    for i in range(ligne):
        temp = []
        for j in range(colonne):
            s = 0
            for k in range(c):
                s += A[i][k] * B[k][j]
            temp.append(s)
        p.append(temp)
    print(p)
    return p

def variables(Mat):
    v = []
    for i in range(1,len(Mat)+1):
        temp = [f'x{i}']
        v.append(temp)
    print(v)

def valeurPropre(Mat):
    return (Mat[0][0] * Mat[1][1]) - (Mat[0][1] * Mat[1][0])

if __name__ == "__main__":
    A = [
        [1,1,1],
        [1,0,1],
    ]
    
    B = [
        [1,1],
        [1,0],
        [1,1]
    ]
    
    Mat = produit(transposed(B), transposed(A))
    variables(Mat)