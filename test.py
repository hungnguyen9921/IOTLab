from sympy import symbols, sympify
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import T
from sympy import *
import numpy as np
from sympy import Symbol, S, tan, log, pi, sqrt
from sympy.sets import Interval
from sympy.calculus.util import continuous_domain

x = symbols("x")

inputValue = input("Please enter a function that you want to caculate:\n")
lowerBound = int(input("Enter lower bound: "))
upperBound = int(input("Enter upper bound: "))
k = int(input("Please enter a k that you want: "))
tempInput = parse_expr(inputValue, transformations=T[:6])
continuos = continuous_domain(tempInput, x, Interval(lowerBound, upperBound)) == Interval(lowerBound, upperBound)
if continuos == True:

    f = tempInput.diff(x)
    f = f.diff(x)
    if f != 0:
        value = []
        temp = lowerBound 
        tempk = 10**k + 1
        for i in range(1000):
            if(i == 0):
                xtemp = 0
            else:
                xtemp = (upperBound - lowerBound)/ 1000

            temp = temp + xtemp
            valuetemp = abs(f.subs(x,temp))
            value.append(valuetemp)

        # value = [f for x in np.linspace(0,1,1000)]
        maxvalue = np.max(value)

        minimunN = (maxvalue*((upperBound-lowerBound)**3))/(3*(10**(-k)))
        N = round(sqrt(minimunN))

        CountK = 1
        temp = ((N + 1)*(10**(-1)))/2
        while(temp >= ((10**(-k))/4)):
            CountK = CountK + 1
            temp = ((N + 1)*(10**(-CountK)))/2

        Xi = []
        Yi = []
        Ai = []
        Aivar = []

        for i in range(N+1):
            temp = lowerBound + i*(upperBound-lowerBound)/N 
            Xi.append(temp)
            Yi.append(tempInput.subs(x,temp))
            if i == 0:
                Ai.append((upperBound-lowerBound)/N*(tempInput.subs(x,temp))/2)
                Aivar.append(round((upperBound-lowerBound)/N*(tempInput.subs(x,temp))/2,CountK))
            elif(i == N):
                Ai.append((upperBound-lowerBound)/N*(tempInput.subs(x,temp))/2)
                Aivar.append(round((upperBound-lowerBound)/N*(tempInput.subs(x,temp))/2,CountK))
            else:
                Ai.append((upperBound-lowerBound)/N*(tempInput.subs(x,temp)))
                Aivar.append(round((upperBound-lowerBound)/N*(tempInput.subs(x,temp)),CountK))

        It = sum(Ai)
        Itvar = sum(Aivar)
        print("Final result:", round(Itvar,CountK))
    else:
        print("Final result: 0",)

else:
    print("Function", continuous_domain(tempInput, x, Interval(lowerBound, upperBound)))

