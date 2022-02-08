import lexico 
import sintatico

def AL(fileMjava):
    aLexico = lexico.Lexico(fileMjava)
    aLexico.executaLexico()
    aLexico.close()
    
    aSintatico = sintatico.Sintatico(fileMjava)
    aSintatico.executaSintatico()
    aSintatico.close()


if __name__ == '__main__':
    AL("test.mjava")
