#Fibonacci
def fibonacci(n):
    if n < 0:
        return None
    elif n==0:
        return 0
    if n==1:
        else
            return fibonacci(n-1) + fibonacci(n-2)



def fibonacci(n):
    """ compute the nth Fibonacci number """

    if n < 0:
        return None
    elif n == 0:
        return 0
    if n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(12))
