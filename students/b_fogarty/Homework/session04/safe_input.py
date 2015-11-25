def safe_input(x):
    try:
        input(x) 
    except EOFError or KeyboardInterrupt:
        print('None')