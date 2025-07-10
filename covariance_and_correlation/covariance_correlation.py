from collections import defaultdict

from test_datasets import data1, data2, data3, data4, data5

data = [data1, data2, data3, data4, data5]


''' We need to determine whether two discrete random variables are independent, 
and return the covariance if so (which should just be zero?), the correlation if not.

Two discrete random variables are independent if and only if their joint probability 
distribution collapses to the product of their marginal distributions

    P(X = x, Y = y) = P(X = x) * P(Y = y) for all (x, y)

The joint probability distribution can be calculated using the chain rule for 
probabilities:

    P(X, Y) = P(X) . P(Y | X) ; (P(Y | X) should just be P(Y) if they are independent)

If this condition is true (these calculations return the same joint probability), then the variables are independent, 
therefore they are uncorrelated and their covariance is 0:

    cov(X, Y) = 0

However, the converse is not true. If cov(X, Y) = 0, the variables are uncorrelated but 
not necessarily independent.

Covariance measures how much two variables vary together, and is calculated as 
the expected value of the product of their deviations from their means
    
    cov(X,Y) = E[(X-E[X])*(Y-E[Y])] = E[XY]-E[X]E[Y]

Correlation coefficients are the normalised version of covariance, calculated by dividing the covariance by the product of the variable standard deviations

    corr(X, Y) = cov(X, Y) / (STD(X) * STD(Y)) = cov(X, Y) / (root(var(X)) * root(var(Y))) = cov(X, Y) / (root(cov(X, X)) * root(cov(Y, Y))) (covariance with self is variance)

'''

''' to check if two discrete random variables are independent, the joint probability needs equate to the product of the marginal probabilities.

If they are not independent, the covariance is nonzero, and is calculated as cov(X=x), Y=y) = E[XY]-E[X]E[Y]
'''

# print(data)

def mean(arr):
    # returns mean value of array/list

    count = len(arr)
    total = 0

    for x in arr:
        total +=x

    return total/count

def sq_root(num):
    return num**0.5

def cov_calc(sample):
    '''
    Returns covariance of arrays/lists X and Y structured [(x1, y1), (x2, y2)...(xn, yn)]
    '''
    X = []
    Y = []
    XY = []
    for x, y in sample:
        # print(x, y)
        X.append(x)
        Y.append(y)
        XY.append(x*y)

    mu_X = mean(X)
    mu_Y = mean(Y)
    mu_XY = mean(XY)

    return mu_XY-mu_X*mu_Y

def corr_calc(sample):

    cov = cov_calc(sample)

    X = []
    Y = []
    
    for x, y in sample:
        # print(x, y)
        X.append(x)
        Y.append(y)

    var_X = cov_calc([(x, x) for x in X])
    var_Y = cov_calc([(y, y) for y in Y])

    if var_X != 0 and var_Y != 0:
        return cov/(sq_root(var_X)*sq_root(var_Y))
    else:
        return 0

def joint_table_marginals(arr):
    '''given [(x1, y1), ..., (xn, yn)] return join distribution matrix, and marginal probabilities
    probably easier in dictionary joint_table = {(x1, y1): prob(x1, y1), ...} and margins{x:{num_x1: prob(x1)..., num_xi: prob(xi),
                                                                                          y: {....}}
                                                                                          
    will need count of unique entries, and count of individual values'''

    # counts

    X = defaultdict(int)
    Y = defaultdict(int)
    X_Y = defaultdict(int)
    
    for x, y in arr:
        # print(x, y)
        X[x] += 1 
        Y[y] += 1
        X_Y[(x, y)] += 1

    entry_count = len(arr)

    # Probabilities

    X_prob = defaultdict(float)
    Y_prob = defaultdict(float)
    X_Y_prob = defaultdict(float)

    for key, val in X.items():
        X_prob[key] = val/entry_count

    for key, val in Y.items():
        Y_prob[key] = val/entry_count

    for xval in X.keys():
        for yval in Y.keys():
            join_key = ((xval, yval))
            X_Y_prob[join_key] = X_Y[join_key]/entry_count

            if X_Y_prob[join_key] != X_prob[xval]*Y_prob[yval]:
                print(X_Y_prob, X_prob, Y_prob)
                return 'Not independent'

    # Check if P(X, Y) = P(X)*P(Y)

    # for i in range(entry_count):
    #     for j in range(entry_count):
    #         if 
    print(X_Y_prob, X_prob, Y_prob)
    return 'Independent'
    # return(X, Y, X_Y, entry_count)

    
# print('Data: ', data[0],'\nTables: ', joint_table_marginals(data[0]))

for i, arr in enumerate(data[:len(data)-1]):
    print(f'Dataset: ', arr, '\nCovariance: ', cov_calc(arr), '\nCorrelation Coefficient: ', corr_calc(arr), '\nIndependent?:, ', joint_table_marginals(arr))


