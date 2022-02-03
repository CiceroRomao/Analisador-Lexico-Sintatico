import lexico 
#from sintatico import sintatico

def AL(fileMjava):
    al = lexico.Lexico(fileMjava)
    al.executaLexico()
    al.close()


if __name__ == '__main__':
    AL("test.mjava")
