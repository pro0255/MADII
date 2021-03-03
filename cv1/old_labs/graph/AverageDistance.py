def average_distance(floyd_matrix, verbose=False):
    n = len(floyd_matrix)
    suma = 0
    for i in range(n):
        for j in range(i, n):
            suma += floyd_matrix[i][j]
    result = 0
    try:
        result = (2/(n*(n-1)))*suma
    except:
        result = 0

    o =  f'Prumerna vzdalenost - {result}'

    output = f'{o}\n'
    if verbose:
        print(o)
    return (output, result)