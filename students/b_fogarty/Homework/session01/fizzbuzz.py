#class 2 hw

#fizzbuzz
for n in range(1,101):
    if n % 15 == 0:
        print('FizzBuzz')
    elif n % 5 == 0:
        print('Buzz')
    elif n % 3 == 0:
        print('Fizz')
    elif n % 15 != 0 and n % 5 != 0 and n % 3 != 0:
        print(n)
