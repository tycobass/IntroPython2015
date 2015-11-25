#improving input function
def safe_input(text_add)
try:
    text_add = input('Type what you like here > ')
except (EOFError, KeyboardInterrupt):
    print('None')
finally:
    print(text_add)