# def factorial(n):
#     factorial = 1
#     for i in range(1,n+1):
#         factorial *= i
#         print(i)
#         print(factorial )

#     print(factorial) 


# factorial(5) 


# def recursionFact(n):
#     factorial = 1
#     if n == 1:
#         print(factorial)

#     else:
#         # return
#         factorial = factorial   * recursionFact(n-1) 

# recursionFact(5) 

def fiboLoop(n):
    f_i = 0
    f_j = 1

    print(f_i, f_j, end = " ")

    for i in range(2, n):
        
        f_new = f_j + f_i
        f_i = f_j
        f_j = f_new
        print(f_new, end = " ")

        

    # print(f_new)

fiboLoop(8)   




