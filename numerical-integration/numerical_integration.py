import math

def integrate(f, a, b, n):
    '''
    Approximates the integral of function f, between the bounds of [a, b] 
    by applying the trapezoid rule over n steps/interval
    
    THe trapezoid rule approximates the integral of a piecewise continuous function
    over the interval from a to b, by summing the areas of n trapezoids defined by the 
    x-axis and two points, f(x_i) and f(x_i+h)
    
    The can be expressed as 
        integral(f(x))_a^b = h/2*(f(a)+f(b)+2*sum(f(x1), f(x2),... f(n))) -> notice the 1/2 and 2*'s cancel for the intermediate terms

        where h = (b-a)/n and the interval is 
        '''
    
    if n < 1:
        return('Invalid steps n; should be integer > 0')

    h = (b-a)/n

    # intialise before loop
    area = (f(a)+f(b))

    for i in range(1, n):
        area += 2*f(a+i*h)

    return area*h/2

def f1(x):
    return(math.sin(x))

b = math.pi

for n in range(0, 100, 2):
    print(f'Steps: {n}  | Area 0-{b}: {integrate(f1, 0, b, n)}')