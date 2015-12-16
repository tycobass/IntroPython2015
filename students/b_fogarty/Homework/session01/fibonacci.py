#Fibonacci
def fibonacci(n):
    for x in range(0,n+1):
        x+=x
    print(x)

fibonacci(12)