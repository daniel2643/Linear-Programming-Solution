
from numpy import *
import sys

def simplex(obj_func, inequlaities_constriants):
    top = obj_func.copy()

    # 1. initialization, make equation matrix rep, make objective function list rep
    ndecision = len(obj_func)
    nslack = len(inequlaities_constriants)    # num(constraints) == num(slacks)

    # equation matrix rep
    equations = []
    for index, inequlaity in enumerate(inequlaities_constriants):
        cache = []

        # add decision variables
        for i in range(ndecision):
            cache.append(inequlaity[i])

        # add slack variables to make inequality to equation
        for i in range(nslack):
            if i == index:
                cache.append(1)
            else:
                cache.append(0)

        # add RHS (i.e. constant)
        cache.append(inequlaity[-1])

        equations.append(cache)
    for coes in equations: print(coes)

    # objective function list rep
    cache = []
    for i in range(ndecision):
        cache.append(obj_func[i])
    cache += ([0]*nslack + [0])
    obj_func = cache.copy()   # obj_func [coefficients...., Z]
    print("START:::::", obj_func, "\n\n\n")


    a=1
    ### 2. simplex
    while a < 7:
        a+=1
        # find the max coefficient in objective function
        maximal = obj_func[0]
        var_index = 0    # the index of variable to be change(increase/decrease) in next iteration to improve Z
        for i in range(1, len(obj_func)-1):
            if obj_func[i] > maximal:
                maximal = obj_func[i]
                var_index = i
        if maximal <= 0:
            break
        print("max && var_index:", maximal, var_index)

        # calculate θ && ensure next interation start calculation row index
        θ = equations[0][-1]/equations[0][var_index]
        o = [θ]
        out_row_index = 0   # the index of largest θ
        for i in range(1, nslack):
            o.append(equations[i][-1]/equations[i][var_index])
            if 0 < equations[i][-1]/equations[i][var_index] < θ:
                θ = equations[i][-1]/equations[i][var_index]
                out_row_index = i
        print("θ: ", o, θ)


        # next iteration
            # fill equation matrix
                # start row
        intersection = equations[out_row_index][var_index]
        start_row = [el/intersection for el in equations[out_row_index]]
        equations[out_row_index] = start_row.copy()

                # other rows
        for i in range(nslack):
            if i != out_row_index:
                equations[i] = [equations[i][j] - start_row[j]*equations[i][var_index]/start_row[var_index] for j in range(len(equations[i]))]

            # fill objective function
        z = obj_func[-1] + start_row[-1]*obj_func[var_index]/start_row[var_index]
        obj_func = [obj_func[j] - start_row[j]*obj_func[var_index]/start_row[var_index] for j in range(len(obj_func))]
        obj_func[-1] = z


        for coes in equations:
            print(coes)
        print("OBJECTIVE FUNCTION:", obj_func, "\n")

    return obj_func[-1]







if __name__ == '__main__':
    print(simplex(sys.argv[1], sys.argv[2]))
#   sys.argv[1]: objective function represented by a matrix
#   sys.argv[2]: constraints represented by a matrix
