p = '+ '
m = '- '
b = '|         '
top = p + (m * 4) + p + (m * 4) + p
bottom = b*3 + "\n"
print(top)
print(bottom*4)

def grid(dim):
    p = '+ '
    m = '- '
    b = '|         '
    top = p + (m * p + "\n"
    side = b*3 + "\n"
    return(top + side * (dim-1) + top)

grid(11)