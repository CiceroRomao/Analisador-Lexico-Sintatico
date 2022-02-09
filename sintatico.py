import pandas

class Sintatico:
    def __init__(self, file):
        self.file = open(file)
        self.fileAux = file
        self.AnaliseSintatica = pandas.DataFrame(columns=["Lexema","Padrão","Token","Linha"])
        self.errosSintaticos = pandas.DataFrame(columns=["Lexema","Padrão","Token","Linha"])
        
        
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
        
        self.TiposIds = [
            "int",
            "boolean",
            "double",
            "float"
        ]
        
        
        self.structPublicMain = [
            "public",
            "static",
            "void",
            "main",
            "(",
            "String",
            "[",
            "]",
            "a",
            ")",
            "{"
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
        
        self.operatorsOfMath = [
            "=",
            "+",
            "-",
            "*",
            "/",
            "%"
        ]
        
        self.vetCPC = []
        
        
    #Função para printar resultado
    def executaSintatico(self):
        self.mainClass()
        self.confereOp()   
            
        #converte o datagrama para arquivo de texto
        self.errosSintaticos.to_csv(r'Análise Sintática.txt', header=None, index=None, sep=' ', mode='a')
        
                
                
          
    def mainClass(self):
        tokenAtual = ""
        tokenPosterior = ""
        numLinhas = 0
        fechamento = 0
        
        for line in self.file:
            numLinhas += 1
            i = 0
            if fechamento == 0 or numLinhas > fechamento:
                while i < len(line):
                    aux = i + 1
                    if line[i] != "" and line[i] != " " and line[i] != "\n":
                        tokenAtual += line[i]
                        print(tokenAtual)
                        if tokenAtual in self.reservedStrings or tokenAtual in self.operators:
                            if tokenAtual in self.reservedStrings and tokenAtual != "else":
                                tokenPosterior = self.buscaTokenPosterior(tokenAtual, numLinhas)
                                
                                if tokenAtual == "public":
                                    if tokenPosterior == "static":
                                        self.confereStructPublic(tokenAtual, numLinhas)
                                        tokenAtual = ""
                                    elif tokenPosterior not in self.reservedStrings and tokenPosterior not in self.operators:
                                        self.insereErro(tokenPosterior , numLinhas)     
                                        tokenPosterior = ""                                      
                                        tokenAtual = ""  
                                    elif tokenPosterior in self.TiposIds:
                                        self.insereLinha(tokenPosterior , numLinhas)     
                                        tokenPosterior = ""                                      
                                        tokenAtual = ""
                                    elif tokenPosterior in self.reservedStrings:
                                        self.insereLinha(tokenPosterior , numLinhas)     
                                        tokenPosterior = ""                                      
                                        tokenAtual = ""
                                        
                                else:                                        
                                    if tokenPosterior != None and str.isdigit(tokenPosterior):
                                        self.insereErro(tokenPosterior , numLinhas)     
                                        tokenPosterior = ""
                                    elif tokenPosterior == None:
                                        self.insereErro(tokenAtual , numLinhas)     
                                        tokenPosterior = ""
                                        
                                self.insereLinha(tokenAtual , numLinhas)      
                                tokenAtual = ""
                                tokenPosterior = ""
                                    
                            elif tokenAtual in self.operators:
                                if tokenAtual == "/":
                                    if line[aux] != "/" and line[aux] != "*":
                                        self.insereLinha(tokenAtual, numLinhas)
                                        tokenAtual = ""
                                    elif line[aux] == "/":
                                        self.AnaliseSintatica = self.AnaliseSintatica.append(
                                        {"Lexema": "//", "Padrão": "Comment", "Token": "<//,"+ str(numLinhas) +">", "Linha": numLinhas},
                                        ignore_index=True)
                                        tokenAtual = ""
                                        break
                                    elif line[aux] == "*":
                                        self.AnaliseSintatica = self.AnaliseSintatica.append(
                                        {"Lexema": "/*", "Padrão": "Comment", "Token": "</*,"+ str(numLinhas) +">", "Linha": numLinhas},
                                        ignore_index=True)
                                        tokenAtual = ""
                                        fechamento = self.confereFechamento(numLinhas)
                                        tokenAtual = ""
                                        break     
                                    
                                elif tokenAtual == "{" or tokenAtual == "}":
                                    self.insereLinha(tokenAtual, numLinhas)
                                    self.vetCPC += tokenAtual
                                    tokenAtual = ""   
                                                                               
                                elif tokenAtual == "(" or tokenAtual == ")":
                                    self.insereLinha(tokenAtual, numLinhas)
                                    self.vetCPC += tokenAtual
                                    tokenAtual = ""         
                                                                         
                                elif tokenAtual == "[" or tokenAtual == "]":
                                    self.insereLinha(tokenAtual, numLinhas)
                                    self.vetCPC += tokenAtual
                                    tokenAtual = ""                                              
                                
                                print(tokenAtual)        
                                self.insereLinha(tokenAtual, numLinhas)
                                tokenAtual = ""
                                
                        elif line[aux] == "" or line[aux] == " " or line[aux] == "\n" or line[aux] in self.operators:                            
                            if line[aux] == "\n":
                                self.insereErro(tokenAtual, numLinhas)
                                tokenAtual = ""
                            elif line[aux] in self.operators or line[aux] == "" or line[aux] == " ":
                                self.insereLinha(tokenAtual, numLinhas)
                                tokenAtual = ""
                    i += 1    
     
    
    def confereStructPublic(self, token, numLinha):
        auxFile = open(self.fileAux)
        numLinhaAtual = 0
        tokenAtual = ""
        aux = 0
        
        for line in auxFile:
            numLinhaAtual += 1
            if numLinhaAtual == numLinha:
                i = 0
                while i < len(self.structPublicMain):
                    if line[i] != "" and line[i] != " " and line[i] != "\n":
                        tokenAtual += line [i]
                        if line[i+1] == "" or line[i+1] == " " or line[i+1] == "/n":
                            if tokenAtual != self.structPublicMain[aux]:
                                if self.structPublicMain[aux] == "a":
                                    self.insereLinha(tokenAtual, numLinhaAtual)    
                                    aux += 1    
                                else:
                                    self.insereErro(tokenAtual, numLinhaAtual)
                                    aux += 1
                            else:
                                self.insereLinha(tokenAtual, numLinhaAtual)    
                                aux += 1
                    i += 1
         
    
    def confereOp(self):
        i = 0
        contChavesAbertura = 0
        contChavesFechamento = 0
        contColcheteAbertura = 0
        contColcheteFechamento = 0
        contParentsAbertura = 0
        contParentsFechamento = 0
        
        j = 0
        while j < len(self.vetCPC):
            print(self.vetCPC[j])
            j += 1

        while i < len(self.vetCPC):
            if self.vetCPC[i] == "{":
                contChavesAbertura += 1
            elif self.vetCPC[i] == "}":
                contChavesFechamento += 1
            elif self.vetCPC[i] == "(":
                contParentsAbertura += 1
            elif self.vetCPC[i] == ")":
                contParentsFechamento += 1
            elif self.vetCPC[i] == "[":
                contColcheteAbertura += 1
            elif self.vetCPC[i] == "]":
                contColcheteFechamento += 1
            i += 1                    
                
        if contChavesAbertura != contChavesFechamento:
            if contChavesAbertura > contChavesFechamento:
                auxFile = open(self.fileAux)
                numLinha = 0
                for line in auxFile:
                    numLinha += 1
                    i = 0
                    token = ""
                    while i < len(line):
                        if line[i] != "" and line[i] != " " and line[i] != "\n":
                            token += line[i]
                            if token == "{":
                                self.errosSintaticos = self.errosSintaticos.append(
                                {"Lexema": token,"Padrão":"ErroAoAbrir","Token":"<"+str(token)+","+ str(numLinha) +">" ,"Linha": numLinha},
                                ignore_index=True)
                                token = ""
                            elif token in self.reservedStrings or token in self.operators:
                                token =""    
                            elif str.isdigit(token):
                                token = ""
                            elif line[i+1] == "" or line[i+1] == " " or line[i+1] == "\n":
                                token = ""
                            elif line[i+1] in self.operators:
                                token = ""
                        i += 1
                        
            elif contChavesAbertura < contChavesFechamento:                     
                auxFile = open(self.fileAux)
                numLinha = 0
                for line in auxFile:
                    numLinha += 1
                    i = 0
                    token = ""
                    while i < len(line):
                        if line[i] != "" and line[i] != " " and line[i] != "\n":
                            token += line[i]
                            if token == "}":
                                self.errosSintaticos = self.errosSintaticos.append(
                                {"Lexema": token,"Padrão":"ErroAoFechar","Token":"<"+str(token)+","+ str(numLinha) +">" ,"Linha": numLinha},
                                ignore_index=True)
                                token = ""
                            elif token in self.reservedStrings or token in self.operators:
                                token =""    
                            elif str.isdigit(token):
                                token = ""
                            elif line[i] == "" and line[i] == " " and line[i] == "\n":
                                token = ""
                        i += 1
  
        elif contParentsAbertura != contParentsFechamento:
            if contParentsAbertura > contParentsFechamento:
                auxFile = open(self.fileAux)
                numLinha = 0
                for line in auxFile:
                    numLinha += 1
                    i = 0
                    token = ""
                    while i < len(line):
                        if line[i] != "" and line[i] != " " and line[i] != "\n":
                            token += line[i]
                            if token == "(":
                                self.errosSintaticos = self.errosSintaticos.append(
                                {"Lexema": token,"Padrão":"ErroAoAbrir","Token":"<"+str(token)+","+ str(numLinha) +">" ,"Linha": numLinha},
                                ignore_index=True)
                                token = ""
                            elif token in self.reservedStrings or token in self.operators:
                                token =""    
                            elif str.isdigit(token):
                                token = ""
                            elif line[i+1] == "" or line[i+1] == " " or line[i+1] == "\n":
                                token = ""
                            elif line[i+1] in self.operators:
                                token = ""
                        i += 1
                        
            elif contParentsAbertura < contParentsFechamento:                     
                auxFile = open(self.fileAux)
                numLinha = 0
                for line in auxFile:
                    numLinha += 1
                    i = 0
                    token = ""
                    while i < len(line):
                        if line[i] != "" and line[i] != " " and line[i] != "\n":
                            token += line[i]
                            if token == ")":
                                self.errosSintaticos = self.errosSintaticos.append(
                                {"Lexema": token,"Padrão":"ErroAoFechar","Token":"<"+str(token)+","+ str(numLinha) +">" ,"Linha": numLinha},
                                ignore_index=True)
                                token = ""
                            elif token in self.reservedStrings or token in self.operators:
                                token =""    
                            elif str.isdigit(token):
                                token = ""
                            elif line[i] == "" and line[i] == " " and line[i] == "\n":
                                token = ""
                        i += 1
           
        elif contColcheteAbertura != contColcheteFechamento:    
            if contColcheteAbertura > contColcheteFechamento:
                auxFile = open(self.fileAux)
                numLinha = 0
                for line in auxFile:
                    numLinha += 1
                    i = 0
                    token = ""
                    while i < len(line):
                        if line[i] != "" and line[i] != " " and line[i] != "\n":
                            token += line[i]
                            if token == "[":
                                self.errosSintaticos = self.errosSintaticos.append(
                                {"Lexema": token,"Padrão":"ErroAoAbrir","Token":"<"+str(token)+","+ str(numLinha) +">" ,"Linha": numLinha},
                                ignore_index=True)
                                token = ""
                            elif token in self.reservedStrings or token in self.operators:
                                token =""    
                            elif str.isdigit(token):
                                token = ""
                            elif line[i+1] == "" or line[i+1] == " " or line[i+1] == "\n":
                                token = ""
                            elif line[i+1] in self.operators:
                                token = ""
                        i += 1
                        
            elif contColcheteAbertura < contColcheteFechamento:                     
                auxFile = open(self.fileAux)
                numLinha = 0
                for line in auxFile:
                    numLinha += 1
                    i = 0
                    token = ""
                    while i < len(line):
                        if line[i] != "" and line[i] != " " and line[i] != "\n":
                            token += line[i]
                            if token == "]":
                                self.errosSintaticos = self.errosSintaticos.append(
                                {"Lexema": token,"Padrão":"ErroAoFechar","Token":"<"+str(token)+","+ str(numLinha) +">" ,"Linha": numLinha},
                                ignore_index=True)
                                token = ""
                            elif token in self.reservedStrings or token in self.operators:
                                token =""    
                            elif str.isdigit(token):
                                token = ""
                            elif line[i] == "" and line[i] == " " and line[i] == "\n":
                                token = ""
                        i += 1   
        
    
                 
    def buscaTokenPosterior(self, tokenAtual, numLinha):
        AuxFile = open(self.fileAux)
        tokenPosterior = ""
        tokenAnalisado = ""
        numLinhaAtual = 0
        controle = 0
        for line in AuxFile:
            numLinhaAtual += 1
            i = 0
            if numLinhaAtual == numLinha:
                while i < len(line):
                    if line[i] != "" and line[i] != " " and line[i] != "\n":
                        tokenAnalisado += line[i]
                        if controle == 1:
                            if line[i+1] == "" or line[i+1] == " " or line[i+1] == "\n":
                                tokenPosterior = tokenAnalisado
                                return (tokenPosterior) 
                            elif line[i+1] in self.operators:
                                tokenPosterior = tokenAnalisado
                                return (tokenPosterior)       
                            
                        elif tokenAnalisado == tokenAtual:
                            controle = 1
                            tokenAnalisado = ""                                                        

                        elif line[i+1] == "" or line[i+1] == " " or line[i+1] == "\n":
                            tokenAnalisado = ""
                        
                        elif line[i+1] in self.operators:
                            tokenAnalisado = ""
                            
                        elif tokenAnalisado in self.operators:
                            tokenAnalisado = ""
                                
                    
                    i += 1        
                    
    
            
    def confereFechamento(self, numLinha):
        auxFile = open(self.fileAux)
        numLinhasAtual = 0
        for line in auxFile:
            numLinhasAtual += 1
            if numLinhasAtual >= numLinha:
                if "*/" in line:
                    self.AnaliseSintatica = self.AnaliseSintatica.append(
                    {"Lexema": "*/", "Padrão": "Comment", "Token": "<*/,"+ str(numLinhasAtual) +">", "Linha": numLinhasAtual},
                    ignore_index=True)
                    return(numLinhasAtual) 
                
                   
       
    def insereErro(self, aux, cont):
        if aux in self.reservedStrings:
            self.errosSintaticos = self.errosSintaticos.append(
            {"Lexema": aux,"Padrão":"ReservedString","Token":"<"+str(aux)+","+ str(cont) +">" ,"Linha": cont},
            ignore_index=True)
        elif aux in self.operators:
            self.errosSintaticos = self.errosSintaticos.append(
            {"Lexema": aux,"Padrão":"Operators","Token":"<"+str(aux)+","+ str(cont) +">" ,"Linha": cont},
            ignore_index=True)
        elif str.isdigit(aux):
            self.errosSintaticos = self.errosSintaticos.append(
            {"Lexema": aux,"Padrão":"Number","Token":"<"+str(aux)+","+ str(cont) +">" ,"Linha": cont},
            ignore_index=True)
        else:        
            self.errosSintaticos = self.errosSintaticos.append(
            {"Lexema": aux,"Padrão":"identifier","Token":"<"+str(aux)+","+ str(cont) +">" ,"Linha": cont},
            ignore_index=True)   
                    
    #Função para orgnaizar as linhas no Datagrama
    def insereLinha(self, aux, cont):
        tokenAtual = self.conferirToken(aux, cont)
        padrao = self.conferePadrao(aux)
        self.AnaliseSintatica = self.AnaliseSintatica.append(
            {"Lexema": aux, "Padrão": padrao, "Token": tokenAtual, "Linha": cont},
            ignore_index=True)
    
    #Função para conferir se é um numeral ou indentificador
    def conferirToken(self, aux, cont):
        if aux not in self.reservedStrings and aux not in self.operators:
            if str.isdigit(aux):
                return "<Number,"+ str(cont) +">"   
            return "<Identifier,"+ str(cont) +">"
        return "<"+ aux +","+ str(cont) +">"

    #Função para conferir se é simbolo da linguagem ou palavra reservada ou numeral
    def conferePadrao(self, aux):
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
                
   
