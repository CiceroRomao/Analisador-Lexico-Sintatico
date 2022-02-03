from numpy import number
import pandas

class Lexico:
    def __init__(self, file):
        self.file = open(file)
        self.fileAux = file
        self.saida = pandas.DataFrame(columns=["Lexema","Padrão","Token","Linha"])
        self.errosLexicos = pandas.DataFrame(columns=["Lexema","Padrão","Linha"])
        self.reservedStrings = [
            "boolean",
            "class",
            "extends",  
            "public",
            "static",
            "void",
            "main",
            "String",
            "return",
            "int",
            "if",
            "else",
            "while",
            "System.out.println",
            "length",
            "true",
            "false",
            "this",
            "new"
            ]
        
        self.operators = [
            "(",
            ")",
            "[",
            "]",
            "{",
            "}",
            ";",
            ".",
            ",",
            "=",
            "<",
            "==",
            "!=",
            "+",
            "-",
            "*",
            "/",
            "&&",
            "!"
            ]
    
    
    #Função para printar resultado
    def executaLexico(self):
        self.mainClass()
        
        #converte o datagrama para arquivo de texto
        #self.saida.to_chavesv(r'pandas.txt', header=None, index=None, sep=' ', mode='a')
        #self.errosLexicos.to_chavesv(r'errosLexicos.txt', header=None, index=None, sep=' ', mode='a')
        print(self.saida)
        print(self.errosLexicos)
        print(self.operators)
    
    
    def mainClass(self):
        token = ""
        numLinhas = 0
        for line in self.file:
            numLinhas += 1
            i = 0
            aux = 0
            while i < len(line):
                if line[i] != "" and line[i] != " " and line[i] != "\n":
                    token += line[i]
                    if token in self.reservedStrings or token in self.operators:  
                        if token in self.operators:
                            posistionL = self.confereFechamento(token, numLinhas)
                            if posistionL != 0:
                                if int(posistionL) > 0:
                                    self.errosLexicos = self.errosLexicos.append(
                                    {"Lexema": "{", "Padrão": "operators","Linha": posistionL},
                                    ignore_index=True)                     
                                    optk = 0
                                    posistionL = 0                
                                elif int(posistionL) < 0:
                                    self.errosLexicos = self.errosLexicos.append(
                                    {"Lexema": "}", "Padrão": "operators","Linha": (posistionL * -1)},
                                    ignore_index=True)                     
                                    optk = 0
                                    posistionL = 0                                   
                        self.insereLinha(token , numLinhas)   
                        token = ""
                    elif line[i+1] == " " or line[i+1] == "\n" or line[i+1] in self.operators:                            
                            self.insereLinha(token, numLinhas)
                            token = ""
                i += 1             
        
    ''' 
    TENTAR AJEITAR ESSA FUNÇÃO DENOVO DEPOIS
    #Função responsável por conferir comentários // /**/
    def confereComents(self, aux, linha):
        auxFile = open(self.fileAux)
        auxFile1 = open(self.fileAux)    
        numLinhas = 0
        for percorre in auxFile:
            numLinhas += 1
            if numLinhas == linha:
                if "//" in percorre:
                    return "//"
                elif "/*" in percorre:
                    linhascoments = 0
                    for percorre2 in auxFile1:
                        linhascoments += 1
                        if "*/" in percorre2:
                            return(linhascoments)
        print("")    
    '''
        
    #ACHO QUE ESSA FUNÇÃO PERTENCE A ANALISE SINTÁTICA
    #
    ##
    #
    ##
    #
    #Função responsável por conferir o fechamento dos operadores como {}, () e []        
    def confereFechamento(self, operador, linha):
        auxFile = open(self.fileAux)
        auxFile2 = open(self.fileAux)
        
        if operador == "{":
            chavesFrontais = 0
            chavesInversa = 0
            numLinhas = 0
            
            for percorre in auxFile:
                numLinhas += 1
                i = 0
                while i < len(percorre):
                    if percorre[i] == "{":
                        chavesFrontais += 1
                    elif percorre[i] == "}":
                        chavesInversa += 1
                    i += 1

            if chavesFrontais/2 != 0:
                numLinha = 0
                aux = 0
                for percorre in auxFile2:
                    numLinha += 1
                    i = 0
                    while i < len(percorre):
                        if percorre[i] == "{":
                            aux += 1
                            if aux == chavesFrontais:
                                return (numLinha)
                        i += 1    
                                      
            elif chavesInversa/2 != 0:
                numLinha = 0
                aux = 0
                for percorre in auxFile2:
                    numLinha += 1
                    i = 0
                    while i < len(percorre):
                        if percorre[i] == "}":
                            aux += 1
                            if aux == chavesInversa:
                                return (-numLinha)
                        i += 1    
            return(0)                
                            
                            
                        
            
                        
                    
        elif operador == "(":
            numLinhas = 0
            for percorre in auxFile:
                numLinhas += 1
                if numLinhas >= linha:
                    i = 0
                    while i < len(percorre):
                        if percorre[i] == ")":
                           return("false")
                        i += 1
            return(linha)
        
        elif operador == "[":
            numLinhas = 0
            for percorre in auxFile:
                numLinhas += 1
                if numLinhas >= linha:
                    i = 0
                    while i < len(percorre):
                        if percorre[i] == "]":
                            return("false")
                        i += 1
            return(linha)

                
                
    #Função para orgnaizar as linhas no Datagrama
    def insereLinha(self, aux, cont):
        token = self.conferirNumeral(aux, cont)
        padrao = self.confereGrupo(aux)
        self.saida = self.saida.append(
            {"Lexema": aux, "Padrão": padrao, "Token": token, "Linha": cont},
            ignore_index=True)
    
    #Função para conferir se é um numeral ou indentificador
    def conferirNumeral(self, aux, cont):
        if aux not in self.reservedStrings and aux not in self.operators:
            if aux[0] >= "0" and aux[0] <= "9":
                return "<Number, >"
            return "<Identifier, " + str(cont) + ">"
        return "<" + aux + ",>"

    #Função para conferir se é simbolo da linguagem ou palavra reservada ou numeral
    def confereGrupo(self, aux):
        for r in self.reservedStrings:
            if (r == aux):
                return "ReserverdString"
        for r in self.operators:
            if r == aux:
                return r
        for r in aux:
            if r >= "0" and r <= "9":
                return "Number"
        return "Identifier"

    

    #função para fechar arquivo aberto
    def close(self):
        self.file.close()
        
        
